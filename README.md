<img src="https://github.com/user-attachments/assets/f8d542d9-72a7-4031-8563-0c41549973b3" alt="logo" width="50"/>

<section>
  <div>
    <h1>Inventory API</h1>
    <p align="justify">
      This <b>API</b> was developed to showcase my backend development skills using
      <b>Python</b> and <b>FastAPI</b>. It demonstrates my ability to implement
      complete <b>CRUD</b> functionality, manage the database effectively, and write
      tests to ensure everything operates smoothly and reliably.
    </p>
    <p  align="justify">
      The <b>API</b> includes user authentication with registration and login using <b>JWT</b>,
      without complex profile features. It also provides product management through
      endpoints for creating, listing, updating, and deleting products, allowing full
      <b>CRUD</b> operations for inventory management. Stock control is simplified by endpoints
      for recording stock movements <b>(entry/exit)</b> without excessive details.
    </p>
    <p align="justify">
      The inventory can be queried with endpoints to list all products or view specific
      product details, without advanced filtering. Category management is implemented
      with endpoints to create and edit categories, but without requiring a complex
      category administration system. Finally, automatic documentation is provided using
      <b>FastAPI's</b> built-in features, without the need for additional complex configurations.
    </p>
  </div>

  <div>
    <h2>Technologies</h2>
    <h4>Backend</h4>
    <ul>
      <li>Python 3.12</li>
      <li>FastAPI 0.115.8</li>
    </ul>
    <h4>Database</h4>
    <ul>
      <li>PostgreSQL</li>
    </ul>
    <h4>ORM</h4>
    <ul>
      <li>SQLAlchemy</li>
    </ul>
    <h4>Authentication</h4>
    <ul>
      <li>SQLAlchemy</li>
    </ul>
    <h4>Documentation</h4>
    <ul>
      <li>Swagger and ReDoc</li>
    </ul>
    <h4>Dependency management</h4>
    <ul>
      <li>pip</li>
    </ul>
    <h4>Tests</h4>
    <ul>
      <li>pytest</li>
    </ul>
  </div>

  <div>
    <h2>Services Used</h2>
    <ul>
      <li>GitHub</li>
    </ul>
  </div>

  <div>
    <h2>Getting Used</h2>
  <p align="justify">
    Optionally, you can create a virtual environment by doing the following in the CLI:

  ```
  pip install virtualenv
  ```

  ```
  python -m venv venv
  ```
  </p>

  <p align="justify">
    To activate the virtual environment, execute the command, if activated correctly,
    the name of the virtual environment will appear on the left in the terminal.

  ```
  \venv\Scripts\activate
  ```
  </p>

  <p align="justify">
    To use this project, make a clone of it using <b>GitHub</b> and then run the following command:

  ```
  pip install requirements.txt
  ```
  </p>

  <p align="justify">
    But to work properly, it's necessary to create a <b>PostgreSQL</b> database and create a <b>.env</b> file
    with the following fields:

  ```
  # Database
  DB_USER= # Name of your user in PostgreSQL
  DB_PASSWORD= # Password for your user in PostgreSQL
  DB_HOST= # Host to run the database, generally: localhost
  DB_PORT= # Port to the database, generally: 5432
  DB_NAME= # Database name
  
  # JWT authentication
  SECRET_KEY=B2Ht5AAWaSvfS9XcQhtU
  ALGORITHM= # Algorithm to JWT, like HS256
  ACCESS_TOKEN_EXPIRE_MINUTES= # Time to the token be valid
  ```
  </p>

  <p align="justify">
    To execute this project, then run the following command:

  ```
  uvicorn main:app --reload
  ```
  </p>

  <p align="justify">
    To see the documentation made with <b>Swagger</b>, access the following link: (Optional)

  ```
  http://127.0.0.1:8000/docs
  ```
  </p>

  <p align="justify">
    To see the documentation made with <b>ReDoc</b>, access the following link: (Optional)

  ```
  http://127.0.0.1:8000/redoc
  ```
  </p>

  <p align="justify">
    To run the tests, run the following command: (Optional)

  ```
  pytest --cov=app tests
  ```
  </p>
  </div>

  <div>
    <h2>Features</h2>
    <p>The main features of the application are:</p>
    <ul>
      <li>User Authentication: Registration and login with JWT authentication, without complex profile functionalities.</li>
      <li>Product Management: Endpoints to create, list, edit, and delete products, with full CRUD operations for inventory management.</li>
      <li>Stock Control: Endpoints to register stock movements (in/out) in a simple way, without excessive details.</li>
      <li>Inventory Query: Endpoints to list all products or query a specific product, without advanced filtering.</li>
      <li>Category Management: Endpoints to create and edit categories, without the need for robust category administration.</li>
      <li>Automatic Documentation: Utilization of FastAPI's automatic documentation, without additional complex configurations.</li>
    </ul>
</div>

  <div>
    <h2>Authors</h2>
    <ul>
      <li>
        Eliezer Bergamo
      </li>
    </ul>
  </div>

  <div>
    <h2>Versioning</h2>
    <p>1.0.0</p>
  </div>

  <footer>
    <p align="center">All rights reserved &copy Eliezer Bergamo</p>
  </footer>
</section>
