from django.contrib.auth import authenticate, login, logout
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from hashlib import md5
import json

# Create your views here.
from shop.models import Developer, Player, Transaction, Game, State


def signup(request):
    if request.user.is_authenticated:
        return redirect("shop:index")
    return render(request, 'shop/signup.html')


def logout_view(request):
    logout(request)
    return redirect("shop:login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("shop:index")
    return render(request, 'shop/login.html')


def home(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("shop:index")
        games = Game.objects.all()
        return render(request, "shop/home.html", {"games": games})

    else:
        return HttpResponse(status=500)


def index(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:home")
        if user.groups.filter(name="developers").count() != 0:
            return redirect("shop:developer")
        transactions = Transaction.objects.filter(player=user.player.id)
        purchased_games = []
        for transaction in transactions:
            purchased_games.append(transaction.game)
        return render(request, "shop/index.html", {"user": user, "purchased_games": purchased_games})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request, "shop/login.html", {"error": "One of the fields was empty."})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("shop:index")
        else:
            return render(request, "shop/login.html", {"error": "Wrong username or password."})
    else:
        return redirect("shop:index")


def create(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        developer = False
        try:
            if request.POST['developer']:
                developer = True
        except KeyError:
            developer = False
        print(username, password, email)
        if username is not None and email is not None and password is not None:
            # Checking if strings are empty
            if not username or not email or not password:
                return render(request, "shop/signup.html", {"error": "Please fill in all required fields"})
            if User.objects.filter(username=username).exists():
                return render(request, "shop/signup.html", {"error": "Username already exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "shop/signup.html", {"error": "Email already exists"})
            user = User.objects.create_user(username, email, password)
            if developer:
                # Check if developers group exists
                if Group.objects.filter(name="developers").exists():
                    dev_group = Group.objects.get(name='developers')
                else:
                    Group.objects.create(name='developers').save()
                    dev_group = Group.objects.get(name='developers')
                dev_group.user_set.add(user)
                Developer.objects.create(user=user).save()
            else:
                Player.objects.create(user=user).save()
            user.save()
            login(request, user)
            with mail.get_connection() as connection:
                mail.EmailMessage(
                    "Welcome to the Shop", "We are thrilled to have you!", "games@gameshop.fi", [email],
                    connection=connection,
                ).send()

        return redirect("shop:index")
    else:
        return redirect("shop:signup")


def catalog(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            return redirect("shop:index")
        developers = Developer.objects.all()
        all_games = []
        for developer in developers:
            games = developer.game_set.all()
            for game in games:
                all_games.append(game)
        return render(request, "shop/catalog.html", {"games": all_games})
    else:
        return HttpResponse(status=500)


def game_info(request, game_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            return redirect("shop:index")

        game = get_object_or_404(Game, pk=game_id)
        secret_key = "71ea74c2e09959acf4946ad302674052"
        pid = "mytestsale"
        sid = "SoftwareInc"
        amount = game.price
        success = "https://gameshop-app.herokuapp.com/payment/success/?game_id={}".format(game_id)
        cancel = "https://gameshop-app.herokuapp.com/payment/cancel"
        error = "https://gameshop-app.herokuapp.com/payment/error"
        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
        digest = md5(checksumstr.encode("ascii"))
        checksum = digest.hexdigest()
        url = "http://payments.webcourse.niksula.hut.fi/pay/"
        transaction = Transaction.objects.filter(player=user.player.id, game=game.id)
        if transaction.count() != 0:
            return render(request, "shop/index.html", {"error": "This game is already in your catalog"})
        return render(request, "shop/game_info.html", {"game": game, "url": url, "pid": pid, "sid": sid,
                                                       "amount": amount, "success": success, "cancel": cancel,
                                                       "error": error, "checksum": checksum})
    else:
        return HttpResponse(status=500)


def payment_success(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            return redirect("shop:index")
        game_id = request.GET["game_id"]
        game = get_object_or_404(Game, pk=game_id)
        secret_key = "71ea74c2e09959acf4946ad302674052"
        pid = request.GET["pid"]
        ref = request.GET["ref"]
        result = request.GET["result"]
        checksum = request.GET["checksum"]
        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
        digest = md5(checksumstr.encode("ascii"))
        calculated_checksum = digest.hexdigest()
        print(calculated_checksum)
        print(checksum)
        if checksum == calculated_checksum:
            # Think of try catching and what to do if the DB operation failed.
            Transaction.objects.create(game=game, player=user.player, paid_amount=game.price).save()
            State.objects.create(game=game, player=user.player).save()
            return redirect("shop:index")
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)


def payment_cancel(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            return redirect("shop:index")
        secret_key = "71ea74c2e09959acf4946ad302674052"
        pid = request.GET["pid"]
        ref = request.GET["ref"]
        result = request.GET["result"]
        checksum = request.GET["checksum"]
        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
        digest = md5(checksumstr.encode("ascii"))
        calculated_checksum = digest.hexdigest()
        print(calculated_checksum)
        print(checksum)
        if checksum == calculated_checksum:
            return render(request, "shop/index.html", {"error": "Payment has been cancelled."})
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)


def payment_error(request):
    pass


def play_game(request, game_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            return redirect("shop:index")
        game = get_object_or_404(Game, pk=game_id)
        player = user.player
        transaction = Transaction.objects.filter(game=game_id, player=player.id)
        # Fetch all high scores associated with the currently played game
        if transaction.count() != 0:
            states = State.objects.filter(game=game_id).order_by("-score")
            return render(request, "shop/play_game.html", {"game": game, "states": states})
        else:
            return HttpResponse(status=500)


def developer_view(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            # Statistics for purchased games.
            # Lets get all games if this dev
            games = Game.objects.filter(developer=user.developer.id)
            statistics = []
            for game in games:
                transactions = Transaction.objects.filter(game=game.id)
                for transaction in transactions:
                    statistics.append(transaction)
            return render(request, "shop/developer.html", {"statistics": statistics})
        else:
            return redirect("shop:index")


def developer_games(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            # Render the game list of all games belonging to this developer
            games = user.developer.game_set.all()
            return render(request, "shop/developer_games.html", {"games": games})

        else:
            return redirect("shop:index")


def publish_page_view(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            return render(request, "shop/publish_game_form.html")
        else:
            return redirect("shop:index")


def create_game(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)
        # Makes sure the user is developer
        if user.groups.filter(name="developers").count() == 0:
            return HttpResponse(status=500)
        developer = user.developer
        title = request.POST['title']
        price = request.POST['price']
        url = request.POST['url']
        if not url and not price and not title:
            return render(request, "shop/publish_game_form.html", {"error": "Please fill in all required fields"})
        # Parse the price
        try:
            float_price = float(price)
        except ValueError:
            return render(request, "shop/publish_game_form.html", {"error": "Price is not a number"})
        if float_price <= 0:
            return render(request, "shop/publish_game_form.html", {"error": "Price must be more than 0"})
        # Validate URL
        try:
            URLValidator()(url)
        except ValidationError:
            return render(request, "shop/publish_game_form.html", {"error": "Malformed URL"})
        # Get developer id

        try:
            Game.objects.create(title=title, price=float_price, url=url, developer=developer)
            # URL should be unique(throws Integrity exception)
        except (ValidationError, IntegrityError) as e:
            return render(request, "shop/publish_game_form.html", {"error": "Could not create a game"
                                                                            " (URL should be unique)"})
        return redirect("shop:developer_games")

    else:
        return redirect("shop:signup")


def edit_game(request, game_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        # Makes sure the user is developer
        if user.groups.filter(name="developers").count() == 0:
            return redirect("shop:index")
        game = get_object_or_404(Game, pk=game_id)
        if game.developer.user_id == user.id:
            return render(request, "shop/edit_game.html", {"game": game})
        else:
            return HttpResponse(status=500)

    else:
        return HttpResponse(status=500)


def edit_game_update(request, game_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)
        # Makes sure the user is developer
        if user.groups.filter(name="developers").count() == 0:
            return HttpResponse(status=500)
        game = get_object_or_404(Game, pk=game_id)
        if game.developer.user_id == user.id:
            title = request.POST['title']
            price = request.POST['price']
            url = request.POST['url']
            if not title and not price and not url:
                return render(request, "shop/edit_game.html",
                              {"error": "At least one field must be filled.", "game": game})
            if title.strip():
                Game.objects.filter(pk=game_id).update(title=title)
            if price.strip():
                try:
                    float_price = float(price)
                except ValueError:
                    return render(request, "shop/edit_game.html", {"error": "Price is not a number", "game": game})
                if float_price <= 0:
                    return render(request, "shop/edit_game.html", {"error": "Price must be more than 0", "game": game})
                Game.objects.filter(pk=game_id).update(price=price)
            if url.strip():
                try:
                    URLValidator()(url)
                except ValidationError:
                    return render(request, "shop/edit_game.html", {"error": "Malformed URL", "game": game})
                Game.objects.filter(pk=game_id).update(url=url)
            return redirect("shop:developer_games")

        else:
            return HttpResponse(status=500)

    else:
        return HttpResponse(status=500)


def edit_game_delete(request, game_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)
        # Makes sure the user is developer
        if user.groups.filter(name="developers").count() == 0:
            return HttpResponse(status=500)
        game = get_object_or_404(Game, pk=game_id)
        if game.developer.user_id == user.id:
            Game.objects.get(pk=game_id).delete()
            return redirect("shop:developer_games")

    else:
        return HttpResponse(status=500)


def submit_score(request):
    if request.is_ajax():
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)
        if user.groups.filter(name="developers").count() != 0:
            return HttpResponse(status=500)
        data = request.body.decode("utf-8")
        print(data)
        # try catch the conversion
        json_data = json.loads(data)
        game_id = json_data["game_id"]
        score = json_data["score"]
        game = get_object_or_404(Game, pk=game_id)
        state = State.objects.filter(player=user.player.id, game=game.id)
        if state.count() != 0:
            State.objects.filter(player=user.player.id, game=game.id).update(score=score)
            return JsonResponse({"created": True})
        else:
            return HttpResponse(status=500)


def submit_state(request):
    if request.is_ajax():
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)
        if user.groups.filter(name="developers").count() != 0:
            return HttpResponse(status=500)
        data = request.body.decode("utf-8")
        json_data = json.loads(data)

        game_id = json_data["game_id"]
        game_state = json.dumps(json_data["state"])
        game = get_object_or_404(Game, pk=game_id)
        state = State.objects.filter(player=user.player.id, game=game.id)
        if state.count() != 0:
            State.objects.filter(player=user.player.id, game=game.id).update(state=game_state)
            return JsonResponse(json_data["state"])
        else:
            return HttpResponse(status=500)


def load_game_state(request):
    if request.is_ajax():
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)
        if user.groups.filter(name="developers").count() != 0:
            return HttpResponse(status=500)
        data = request.body.decode("utf-8")
        json_data = json.loads(data)
        game_id = json_data["game_id"]
        game = get_object_or_404(Game, pk=game_id)
        state = State.objects.filter(player=user.player.id, game=game.id)
        if state.count() != 0:
            game_state = state[0].state
            if game_state == "":
                return JsonResponse({"state": game_state, "success": False, "info": "Game state is not set."})
            else:
                return JsonResponse(
                    {"state": json.loads(game_state), "success": True, "info": "Successfully loaded game state"})
        else:
            return HttpResponse(status=500)


def facebook_handler(request):
    if request.method == "GET":
        user = request.user
        if Player.objects.filter(user=user).exists():
            redirect("shop:index")
        else:
            Player.objects.create(user=user).save()
            player = Player.objects.filter(user=user)
            user = player
        return redirect("shop:index")
    return HttpResponse(status=500)


def search(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)
        if user.groups.filter(name="developers").count() != 0:
            return HttpResponse(status=500)
        query = request.POST["q"]
        if not query:
            # Return empty results
            return render(request, "shop/search_result.html", {"error": "Empty search request"})
        games = Game.objects.filter(title__icontains=query)

        return render(request, "shop/search_result.html", {"games": games, "query": query})
    else:
        return redirect("shop:index")
