================================
EasyML-lib
================================

Introduction
------------
EasyML-lib consists of a Python server API (easymlserver) and a simple Android client (easymlclient).

easymlserver is a RESTful API wrapper around Python machine learning libraries scikit-sklearn and python-recsys, as well as a simple data collection and transformation tool.  The eventual goal of easymlserver is to collect event data from mobile apps, store it in a simple CSV file, and then apply optimization, categorization, clustering or recommender system logic to the data.

This library is currently in pre-alpha state - consider it a sketch at this point.  Hopefully in the next few weeks, a slightly more functional build of easymlserver will be found here.

-- May 15th, 2015