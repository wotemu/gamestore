# GameShop

There are two kind of users: developers and players.
A player can purchase games from the gameshop and play those ones he purchased. A developer can upload games, manage his inventory and see sales statistics.


A user registers to the website by filling all required fields. The user can also specify whether he is a player or a developer when registers.
There is third party login system for those who does not want to register to our website. There are two options:login with Facebook.

The website was deployed on the Heroku Platform as a Service (PaaS) at the address: http://gameshop-app.herokuapp.com/

You can test the app by logging in as player or a developer by simply registering.
Our DB has several games to try. In addition try logging in with Facebook, it's so cool :)

We used JetBrains PyCharm, git and GitLab for version control.

Tools, Frameworks and Languages: 

* Bulma CSS framework
* Django 2.0 
* Python 3.6
* Javascript


## Models
* User model 
* Player model (One-to-one relationship to User)
* Developer model (One-to-one relationship to User)
* Game model (One-to-many relationship to Developer)
* Transaction model (Many-to-one relationship to Game and Player)
* State model (Many-to-one relationship to Game and Player)

In addition to differentiate between Players and Developers a Group models was used.

## Views and urls	
For corresponding views please referer to**views.py**
### Main
~~~~
  /create
  /loguser
  /login
  /logout
  /signup
  /home
~~~~
### Developer related
~~~~
 /developer
 /developer/games/<int:game_id>/edit
 /developer/games/<int:game_id>/update
 /developer/games/<int:game_id>/delete
 /developer/mygames
 /developer/publish
 /developer/publish_game
~~~~
### Game state related
~~~~
    /service/score
    /service/state
    /service/load
~~~~
### Player related
~~~~
  /
  /search
  /catalog
  /games/<int:game_id>/info
  /games/<int:game_id>/play
~~~~
### Payment related
~~~~
    /payment/success/
    /payment/cancel
    /payment/error

~~~~
### Facebook related
~~~~
 /facebook
~~~~



