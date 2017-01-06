NTB Pimp
---------

.. image:: https://travis-ci.org/tomkukral/npimp.svg?branch=master
       :target: https://travis-ci.org/tomkukral/npimp

This module is able to regulate your notebook parameters, check states and perform actions. There is this inifite loop:

  - update info objects
  - run actions
  - sleep for 60 seconds

Info modules:

  - Smapi - read information from ThinkPad tp_smapi

Action modules:

  - Dumper - print information from info modules
  - Charging - disable or enable charging according to battery charge (using tp_smapi)
