<h1>Lat2DB Project</h1>

<p>Lat2DB is a project designed to convert lattice files into JSON format and store them in MongoDB. It utilizes a Lark grammar created by Andreas Felix to parse thor_scsi lattice files.</p>
<p> For other lattice formats (e.g. AT) we have separate parsers.</p>

<h2>Features</h2>

<ul>
  <li><strong>Lattice File Conversion</strong>: Lat2DB can read a lattice file and export it to JSON format.</li>
  <li><strong>MongoDB Integration</strong>: The exported JSON data is inserted into MongoDB for efficient storage and retrieval.</li>
  <li><strong>REST API</strong>: Lat2DB is a REST API-based project, built using FastAPI, providing endpoints for interacting with the data.</li>
</ul>

<h2>Getting Started</h2>

<h3>Prerequisites</h3>

<ul>
  <li>Python 3.x</li>
  <li>MongoDB installed and running</li>
</ul>

<h3>Installation</h3>

<ol>
  <li>Clone the repository: <code>git clone &lt;https://github.com/hz-b/lat2db&gt;</code></li>
  <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
  <li>Build UI-> make sure you have Node.js installed and then go to UI directory and run: <code>npm run build</code></li>
</ol>

<h3>Usage</h3>

<h4>Running the REST API</h4>

<p>To start the FastAPI server, run:</p>

<pre><code>python3 scripts/main.py
</code></pre>

<p>The provided API will give you an interface to navigate through different elements of the lattice and even edit them</p>
<p>In order to download the lattice in json format from the api (browser) you can go to the link:</p>
<p>api link followed by /machine/machine/_id of the machine e.g. http://datascc.trs.bessy.de:8000/machine/machine/662f83c50019a6f1a5ce7ea2</p>
<p>The json which is loaded can be saved</p>

<h4>Using the application for calculations</h4>

<p>Go to examples folder and try: create_ring.py or the jupyter file. The examples are self-explanatory</p>

<h4>File Conversion and Insertion</h4>

<p>To convert a lattice file to JSON and insert it into MongoDB, you can use the provided script:</p>

<pre><code>python3 scripts/export_lattice_to_db.py 
</code></pre>

<p>This script will convert the specified lattice file to JSON format and store it in the MongoDB database.</p>

<h2>API Endpoints</h2>

<ul>
  <li><strong>GET <code>/machine/machine</code></strong>: Retrieve a list of existing machines (lattices) from the MongoDB repository.</li>
  <li><strong>GET <code>/machine/machine/&lt;uid&gt;</code></strong>: Retrieve a specific machine by its unique identifier (UID) from the MongoDB repository.</li>
  <li><strong>POST <code>/machine/machine</code></strong>: Create a new machine by posting JSON data.</li>
</ul>

<h2>Acknowledgments</h2>

<p>Thanks to Andreas Felix for the Lark grammar used in this project. <a href="https://github.com/nobeam/latticejson/">Link to Andreas' GitHub Project</a></p>

