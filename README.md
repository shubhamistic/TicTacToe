<h1>TicTacToe README</h1>

<p>A quick multiplayer TicTacToe game designed using (Python-MySQL) and can be triggered directly from the command line.</p>

<h2>INSTALLATION</h2>

<ol>
    <li>clone TicTacToe into your desired folder.</li>
    <code>https://github.com/shubhamistic/TicTacToe.git</code>
    <li>To look at the source code (written in Python) open <code>TicTacToe.py</code></li>
    <li>To play the Game choose the executable file according to your OS</li>
    <ul> 
        <li>TicTacToe FOR WINDOWS</li>
        <li>TicTacToe-m FOR MAC</li>
        <li>TicTacToe-l FOR LINUX</li>
    </ul>      
</ol>

<h2>SETTING UP YOUR PERSONAL MySQL DATABASE</h2>

<p>To setup your personal MySQL database make sure it is accepting remote connection properly.
    <br>
    Now, choose the TicTacToe.py file according to your OS ,
</p>
    <ol>
        <li>After choosing the file click open the file or you can use any editor of your choice if on command line.</li>
        <li>Go to line-74 it will look something like - </li>
        <code>database=mycon.connect(host='example.com',user='YourUser',password='YourPassword',database='YourDatabaseName')</code>
        <li>Enter your host,user,password,database details.</li>
        <li>Do the exact same thing on line-133 , line-230 , line-420 .</li>
        <li>Save the code</li>
    </ol>

