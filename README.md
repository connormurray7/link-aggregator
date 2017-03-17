[Link Aggregator](http://link-aggregator.top) is a website that currently integrates with Github, StackOverflow, and Hacker News API's. It takes a search term, and displays the top results from each site. It uses Redis to cache results in memory and it is written in Python with Flask. Link-agg also uses Gunicorn, and Nginx. See [this article](http://connormurray.me/Deploying-Python/) for how it is deployed.

### _Running locally_

This application is written in Python 3, and it is recommended to use a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for Python. Once the virtual environment is setup you can install the following packages: 

		pip3 install flask gunicorn requests redis

This application requires Redis to run, in the above command you have installed `redis-py` which is a redis client, but the server has not been downloaded yet. For more information on downloading it, [see here](https://redis.io/download). Once Redis is installed, you can start a local server by running `./redis-server`. 

Finally navigate to the `run-locally` directory and execute

	gunicorn --bind 0.0.0.0:8000 wsgi
	
You should then be able to see it running on [http://0.0.0.0:8000/](http://0.0.0.0:8000/) 

### _Why was it built?_
When trying to learn about new topics in software engineering I always would be visiting a bunch of the same sites. Github to see some projects, Hacker News to find some good blog posts/articles on the subject, and Stack Overflow to see some small examples. Instead of searching around every time, I used the APIs from each of sites to aggregate all of the information.
