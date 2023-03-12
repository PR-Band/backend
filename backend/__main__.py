from flask import Flask

from backend import categories, products

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('hello world')
    app.register_blueprint(categories.view, url_prefix='/api/v1/categories')
    app.register_blueprint(products.view, url_prefix='/api/v1/products')

    app.run(port=8000)

if __name__=="__main__":
    main()
