<?php
    require 'check_login_status.php';
?>
<html>
<?php require 'head.php'?>
<body>
<main>
<?php require 'header.php'?>
        <div class="tab" id="tab-2">
            <div class="row">
            <label for="asset-ID-opt-in">Asset-ID:</label>
            <input type="text" id="asset-ID-opt-in" name="asset-ID-opt-in" required >
            </div>
            <div class="row">
            <label for="passphrase-opt-in">Passphrase:</label>
            <input type="text" id="passphrase-opt-in" name="passphrase-opt-in" >
            </div>
            <div class ="row">
        <button type="button" id='sign-opt-in'>
         Opt in
        </button>
        </div>

        <div class="row">
        <div id ="result_opt-in"></div>
        </div>
        </div>
</main>

<?php require 'foot.php' ?>
</body>
</html>