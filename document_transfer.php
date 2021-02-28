<?php
    require 'check_login_status.php';
?>
<html>

<?php require 'head.php' ?>

<body>
<main>
<?php require 'header.php'?>
    <div class="tab" id="tab-3">
            <div class="row">
            <label for="asset-ID-transfer">Asset-ID:</label>
            <input type="text" id="asset-ID-transfer" name="asset-ID-transfer" required >
            </div>
            <div class="row">
            <label for="passphrase-transfer">Passphrase:</label>
            <input type="text" id="passphrase-transfer" name="passphrase-transfer" >>
            </div>
            <div class="row">
            <label for="public-key-other">The destination address :</label>
            <input type="text" id="public-key-other" name="public-key-other" >
            </div>
            <br>
            <div class ="row">
        <button type="button" id='sign-transfer'>
         transfer
        </button>
        </div>

        <div class="row">
        <div id ="result_transfer"></div>
        </div>
        </div>
</main>

<?php require 'foot.php' ?>
</body>
</html>