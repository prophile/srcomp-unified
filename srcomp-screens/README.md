# Student Robotics Competition Screens

This repository contains the web pages for the various screens that are
displayed at the competition.

## Installation & Running

Dependencies are managed with [Bower](http://bower.io/), therefore you must
install them in the normal way:

    $ bower install

The best way to test these screens is to run an HTTP server in the root of your
clone and navigate to it with your web browser.

    $ python3 -m http.server

**Note:** Currently, the screens assume that you will have an `srcomp-stream`
and `srcomp-http` instance running locally on ports 5112 and 5001 respectively.

## Screens

Here are the screens that are in this repository.

### Arena

This screen is displayed in each corner of the arena.

You can configure which corner the screen should be displaying by altering the
query parameters:

    /arena.html?<arena>,<corner>

### Outside

This screen is available to competitors at some strategic points around the
competition venue. It displays information such as the current leaderboard, the
match schedule, the scores and the knockout diagram.

## Components

The screens use [Web Components](http://webcomponents.org/) and
[Polymer](https://www.polymer-project.org/) to make the code more maintainable,
flexible and reusable. They are stored in the `components` folder.
