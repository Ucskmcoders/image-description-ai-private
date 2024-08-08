<body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 20px">
  <h1 style="color: #333">Image Description API</h1>
  <p>
    This project provides a simple HTTP server that generates descriptions for
    images using a pre-trained InceptionV3 model and a simple RNN. The API
    requires an API key for access and allows new API keys to be generated using
    a secret specified in a <code>.env</code> file.
  </p>

  <h2 style="color: #333">Setup Instructions</h2>
  <ol>
    <li>Clone the repository to your local machine.</li>
    <li>Navigate to the project directory.</li>
    <li>Install the required dependencies:</li>
    <pre
      style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
    ><code>pip install tensorflow pillow numpy python-dotenv requests</code></pre>
    <li>
      Create a <code>.env</code> file in the root of the project directory with
      the following content:
    </li>
    <pre
      style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
    ><code>SECRET_KEY=your_secret_key_here</code></pre>
    <li>
      Create an empty <code>api_keys.json</code> file in the root of the project
      directory to store API keys:
    </li>
    <pre
      style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
    ><code>echo "[]" &gt; api_keys.json</code></pre>
    <li>Run the server:</li>
    <pre
      style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
    ><code>python server.py</code></pre>
  </ol>

  <h2 style="color: #333">Deployment on Vercel</h2>
  <ol>
    <li>Initialize a git repository and commit your code:</li>
    <pre
      style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
    ><code>git init<br>git add .<br>git commit -m "Initial commit"</code></pre>
    <li>Login to Vercel using the CLI or web interface.</li>
    <li>Deploy the application:</li>
    <pre
      style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
    ><code>vercel</code></pre>
    <li>Follow the prompts to deploy your application.</li>
  </ol>

  <h2 style="color: #333">Usage</h2>
  <p>
    To use the API, you need a valid API key. If you don't have one, you can
    generate a new API key by providing the secret specified in the
    <code>.env</code> file:
  </p>
  <pre
    style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
  ><code>GET http://your-vercel-app-url/?secret=your_secret</code></pre>
  <p>
    To get a description for an image, make a GET request with your API key and
    the image URL:
  </p>
  <pre
    style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
  ><code>GET http://your-vercel-app-url/?api_key=your_api_key&amp;image_url=image_url</code></pre>
  <p>The response will be a JSON object containing the description:</p>
  <pre
    style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
  ><code>{
    "description": "A man riding a horse"
}</code></pre>

  <h2 style="color: #333">API Key Management</h2>
  <p>
    The API keys are generated using a secret specified in the
    <code>.env</code> file and are stored in the
    <code>api_keys.json</code> file. The keys are hashed using SHA-256 for
    security.
  </p>
  <p>To add a new API key, provide the secret in the request:</p>
  <pre
    style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
  ><code>GET http://your-vercel-app-url/?secret=your_secret</code></pre>
  <p>The response will be a JSON object containing the new API key:</p>
  <pre
    style="background-color: #f4f4f4; padding: 10px; border-radius: 4px"
  ><code>{
    "api_key": "newly_generated_api_key"
}</code></pre>

  <h2 style="color: #333">Security</h2>
  <p>
    Ensure that your <code>.env</code> file is not exposed publicly. The
    <code>.env</code> file contains the secret key used for generating API keys
    and should be kept confidential.
  </p>

  <h4 style="color: #555">Generated using Readme Generator made by harshitkumar9030 @ Github.</h4>
</body>
