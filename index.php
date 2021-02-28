<html>

<?php require 'head.php'?>

<body>
<?php require 'header.php' ?>
    <main>
    <p>
    </p>
        <a href="verify_document.php">Verify any document</a>
        <form method="POST" id="login">
            <h2>Login</h2>
            <div class="form-group row">
                <label for="address">plz enter your passphrase<span class="reminder">*</span>:</label>
                <input type="text" class="form-control" id="passphrase" name="passphrase" >
                <div id = "validate"></div>
            </div>
            <button type="button" id="access" name="access">login</button>
        </form>
        <form  method="POST" id="register" >
            <h2>No account? Register one ! </h2>
            <h5>Press button to generate your own address and passphrase</h5>
            <button type="button" id="create" name="create">Register</button>
        </form>
        <div id ="info"></div>
        <button type="button" id="change" style="display:none;">Next page</button>
    </main>
    <?php require 'foot.php' ?>
</body>
</html>