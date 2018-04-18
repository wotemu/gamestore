# GameShop

Team members:
  - Romanov Aleksandr 664886
  - Umer Khan 599841
  - Tamire workneh 660767
  
## Task Division

We worked in a way that we did not have clear cut division of our tasks.

we started the model design together and we choose the model on which we all agreed.

Every week in meeting we would assign task to each other. we would try to implement 
the required task but most of the time we would get stuck, so we have to discuss it 
one of our group mate @Alex (Experienced and good knowledge), and he would provide us help in solving that issue.
Most of the work that we did follow this pattern, and most of the task we try to solve it together.
so this way every one is aware of the other person task and it helped us to learn a lot.
  
  
## General description of the completed task with Point estimate from each task.
Authentication (mandatory, 100-200 points): 200

Basic player functionalities (mandatory, 100-300 points):  300

Basic developer functionalities (mandatory 100-200 points):  200

Game/service interaction (mandatory 100-200 points): 200

Quality of Work (mandatory 0-100 points) :80

Non-functional requirements (mandatory 0-200 points) :180

Project plan (part of final grading, max. 50 points) :40  

Save/load and resolution feature (0-100 points):  100

3rd party login (0-100 points) :85

RESTful API (0-100 points) :0

Own game (0-100 points) :0

Mobile Friendly (0-50 points): 50

Social media sharing (0-50 points): 0

## Some Issues we encountered

In general the development went quite smoothly. The only obstacles were in:

* Configuring callback URLs for Facebook.
* HTTPS mixed content problem when deploying HTTP based game to Heroku.
* Figuring out how payment service works and developing callback urls (making hidden forms, calculating and validating checksum took some time)

## General Description of Gameshop
This is an online Gameshop developed by three Aalto University students for the Web Software Development course (2017/2018).
The website is developed based on the Django framework, Model-View-Template pattern.

There are two kind of users: developers and players.
A player can purchase games from the gameshop and play those ones he purchased. A developer can upload games, manage his inventory and see sales statistics.
A mockup payment service was provided by the **Aalto University**.

A user registers to the website by filling all required fields. The user can also specify whether he is a player or a developer when registers.
There is third party login system for those who does not want to register to our website. There are two options:login with Facebook.

Our website was deployed on the Heroku Platform as a Service (PaaS) at the address: http://gameshop-app.herokuapp.com/

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




## Minimum functional requirements

#### Register as a player and developer

Done

#### As a developer:

**add games to their inventory, see list of game sales**

Done, a developer can add a new game with title, price and URL to his inventory

#### As a player:

**buy games, play games, see high scores**

Done

#### Authentication

**Login, logout and register (both as player or developer). Use _Django auth_**

Done, we used _Django auth_.

#### Basic player functionality

**Buy games, payment is handled by a mockup payment service (http://payments.webcourse.niksula.hut.fi/) :**

Done, we redirect the user on the payment website after he confirm the order that is shown in the cart.


**Play games. See also game/service interaction**

Done, users can play games, save, load and submit scores.


**Security restrictions, e.g. player is only allowed to play the games they’ve purchased.**

Done, an user can play only at the games that he had purchased.


**Also consider how your players will find games (are they in a category, is there a search functionality?)**

Search is done by game titles.


#### Basic developer functionalities

Done, developers may add games into the system.

Basic game inventory and sales statistics (how many of the developers' games have been bought and when)

developer can delete a game from his inventory.

Done,

#####Problem with developer

One problem with developer deletion is the cascade delete. if a developer delete a game it is also deleted
from the player inventory, because of the cascade delete in our model, which we did not fix.

**Security restrictions, e.g. developers are only allowed to modify/add/etc. their own games, developer can only add games to their own inventory, etc.**

Done, we checked developer can only deal with his own games. From our perspective a developer should not be able to play games, and he needs a separate account. So we perform this kind of checks as well. If the developer cancels the game, every record related to that game is deleted as well, causing a cascade reaction. This may be unsafe in case of orders and statistics (retroactive reactions are possible), however there was no requirement for that feature, so we decided to go for this way.


#### Game/service interaction

When player has finished playing a game (or presses submit score), the game sends a postMessage to the parent window containing the current score. This score must be recorded to the player's scores and to the global high score list for that game. See section on Game Developer Information for details.

Done, used postMessage as requested.

#### Quality of Work

**Quality of code (structure of the application, comments).**
We tried to use the project structure that meets the standards.

**Purposeful use of framework (Don't-Repeat-Yourself principle, Model-View-Template separation of concerns)**
We followed the instructions  given during the lectures.


**User experience (styling, interaction)**
we tried to implement user friendly interaction, so that user can navigate and interact in meaningful way.


##### Problems in quality of work
There are few issue in the quality of our work.

The code is commented but not everywhere.

We have used some inline css, the reason for that was the we used a new CSS framework
in which over riding css was difficult to do.

 
#### Non-functional requirements

**Overall documentation, demo, teamwork, and project management as seen from the history of your GitLab project (and possible other sources that you submit in your final report)**
We had good team spirit and work together. One of our team member has good experience and there was great assistance from him.
We had online and face to face meeting.

our Initial project plan was lacking the useful model implementation since we did not meet before the project plan deadline.

for project management we held online meeting every week and also face meeting when required.
In which we would discuss about the progress of our work and issues.

## More Features


#### Save/load and resolution feature

**The service supports saving and loading for games as described above**
Saving and loading game state for a particular user was not a big issue as we 
designed models to support it.

#### 3rd party login

**Allow OpenID, Gmail or Facebook login to your system. This is the only feature where you are supposed to use third party Django apps in your service.**

We used the django framework, social-auth-app-django, that enables multiple providers.
We focused only on Facebook. This required us to develop a custom pipeline step in order to assign a profile to the social user upon first login.


#### Mobile Friendly
Using Bulma CSS framework we developed the app with the mobile first mindset from the start.


