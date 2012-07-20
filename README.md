ENVMGR
======

IT MANAGES YOUR ENV.

`envmgr` is a simple application that will load environment variables for your app from a directory of config files.

Why would you want to do that? Perhaps you have a suite of applications which all need to know about some common resources, but which also have app-specific configurations. Here's how you'd achieve that with `envmgr`:

    $ ENVMGR_ROOT=~/.envmgr
    $ mkdir -p "$ENVMGR_ROOT"
    $ cd "$ENVMGR_ROOT"
    
    $ cat >common.conf <<EOM
    SQL_URI="postgresql://user:pass@host..."
    ENVIRONMENT=production
    EOM

    $ cat >app_a.conf <<EOM
    include common
    APP_NAME=application_alpha
    USER=maurice
    EOM

    $ cat >app_b.conf <<EOM
    include common
    APP_NAME=application_beta
    USER=norman
    EOM

With your config files created, you can now run your applications through `envmgr`:

    $ envmgr -r "$ENVMGR_ROOT" -n app_a python run_app_a.py
    $ envmgr -r "$ENVMGR_ROOT" -n app_b bundle exec ruby run_app_b.rb


Config syntax
-------------

### `include`

    include other/file

The `include` directive does what it says on the tin: includes directives from another file. In the above example, `envmgr` will attempt to load directives from `$ENVMGR_ROOT/other/file.conf`. 

**NB**: you cannot include files that live outside of `$ENVMGR_ROOT`.

**NB**: `envmgr` makes no attempt to detect cycles when processing the `include` directive. If you create such cycles then expect `envmgr` to blow up in your face.

### `clear`

    clear

Completely clear the environment. When used, this directive will usually come at the beginning of a config file.

### `unset`

    unset HOME

Unset the specified environment variable

### etc.

Any other nonblank lines will be interpreted by `envmgr` as attempts to set an environment variable:

    FOO=bar
    BAR="baz"
    BAZ='bat'

Anything that doesn't conform to one of the above patterns will probably raise a `ParseError` and the baby Jesus will cry. Or something.

As of version 0.0.3, `envmgr` will do some basic interpolation for you:

    NAME=Marcus
    HELLO_MARCUS="Hello, $NAME"       # this will be "Hello, Marcus"
    HELLO_UNDEF="Hello, $IDONTEXIST"  # this will be "Hello, "
    HELLO_SINGLES='Hello, $NAME'      # this will be "Hello, $NAME"

**NB**: one gotcha is that `envmgr` does not use a shell-compliant lexer at the moment, so the following will *not* work as you might expect:

    NAME=Marcus
    HELLO_ESCAPED="Hello \$NAME"      # Gotcha! this will be "Hello \Marcus"

Hacking
-------

Make yourself a [virtualenv](http://virtualenv.org), and then, in a checked out copy of this repository, run:

    pip install -e .

To run the tests, you should do:

    pip install tox
    tox
 
  

