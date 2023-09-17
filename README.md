**Objective**

This Python scripts allow you place, track and delete delivery requests using the uParcel API.

**Requirements**

* Python installed on the machine running this application.
* Credentials for accessing the uParcel API - you need to request to uParcel for the activation of the API for your account. You will then be able to craete your credentials using the uParcel portal.
* Credentials for writing to a MongDB database - this database will be used for logging the responses from the uParcel API.

**How to run this application**

* Copy the file `config-sample.py` to `config.py`.
* Edit `config.py` with your credentials and defaults.
* To place a delivery request, run `python3 req_delivery.py` and follow the instructions of the script.
* To track the status of a delivery request, run `python3 track.py <track_id>`, where `<track_id>` is the uParcel trucking code of your delivery.
* To cancel a delivery request, run `python3 cancel_delivery.py <order_id>`, where `<order_id>` is the Order ID you provided when you made the request *(note that this is NOT the `<track_id>`)*.

**Do you really *need* a MongoDB database?**

* You don't really *need* a database at all, this database is only for logging purposes.

* It is safe to leave the database credentials blank or with bogus data. You will receive an error message each time the script attempts to write to the database, but you can safely ignore this error message.

* The logic behind having a datase is the following though:
  
  * You can pass a WEBHOOK URL to the uParcel API where the API can later post any updates to the delivery request. These updates are posted in JSON format. You will need a database if you are interested in logging these updates. We accomplished that by posting those updates to a MongoDB database.
  
  * The uParcel API posts via the WEBHOOK URL only the events made in their portal, but not the events made via the API, such as the creation or cancellation of the delivery requests by our own scripts, so our scripts will need the ability to post those events to the database too. That is why we added the `push.py` script, which is invoked to do exactly that.
