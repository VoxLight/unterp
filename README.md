<style>
    body {
        font-family: 'Ubuntu', sans-serif;
        background-color: #2c3e50;
        color: #ecf0f1;
        margin: 0;
        padding: 20px;
    }
    h1 {
        color: #ecf0f1;
        text-align: center;
        font-family: 'Consolas', monospace;
    }
    .badges {
        text-align: center;
        margin: 20px 0;
    }
    .badges img {
        margin: 0 10px;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        background: #34495e;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    h2 {
        color: #e67e22;
        border-bottom: 2px solid #e67e22;
        padding-bottom: 5px;
        font-family: 'Consolas', monospace;
    }
    pre {
        background: #1c2833;
        color: #ecf0f1;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
        font-family: 'Consolas', monospace;
    }
    code {
        color: #e74c3c;
        font-family: 'Consolas', monospace;
    }
    table {
        width: 100%;
        margin-top: 20px;
    }
    td {
        vertical-align: top;
    }
    img {
        max-width: 100%;
        border-radius: 8px;
    }
    .contribute {
        text-align: center;
        margin-top: 20px;
    }
</style>
<h1>Unterp - Minimalistic Python Interpreter</h1>
<img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python">
<img src="https://img.shields.io/badge/tkinter-%20UI%20library-red" alt="tkinter">
<img src="https://img.shields.io/badge/Pygments-Syntax%20Highlighting-brightgreen" alt="Pygments">
<img src="https://img.shields.io/badge/License-MIT-green" alt="License">
<p>Welcome to <strong>Unterp</strong>, a minimalistic Python interpreter with a simple and intuitive GUI. This project aims to provide a lightweight alternative to Jupyter notebooks for quick Python script execution and testing.</p>
<h2>Features</h2>
<ul>
    <li><strong>Syntax Highlighting</strong>: Leveraging Pygments for beautiful code highlighting.</li>
    <li><strong>Responsive GUI</strong>: Built with tkinter, providing a clean and responsive user interface.</li>
    <li><strong>Execution Toolbar</strong>: Convenient buttons for running code, clearing the console, and restarting the interpreter.</li>
</ul>
<h2>Installation</h2>
<p>To install the library directly from the GitHub repository, use the following command:</p>
<pre><code>pip install git+https://github.com/voxlight/unterp.git</code></pre>
<h2>Using unterp</h2>
<table>
    <tr>
        <td>
            <p style="font-size:18px;">Just run unterp as a module.</p>
            <pre><code>python -m unterp</code></pre>
        </td>
        <td>
            <img src="./_images/unterp_in_use.jpg" alt="unterp in use">
        </td>
    </tr>
</table>
<h2>Contribute</h2>
<p class="contribute">Feel free to open issues for anything, or make pull requests.</p>
