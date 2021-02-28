<?php
    require 'check_login_status.php';
?>
<html>
<?php require 'head.php'?>
<body>
<main>
<?php require 'header.php'?>
    <form id="createD">
        <div class="tab" id="tab-1">
            <div class="row">
                <label for="doc-name">Document Name :</label>
                <input type="text" id="doc-name" name="doc-name" required size="70">
            </div>
            <div class="row">
                <label for="doc-id">Document ID (short form):</label>
                <input type="text" id="doc-id" name="doc-id" required size="70">
            </div>
            <div class="row">
                <div id="html_file">
                <h6>Please upload your HTML file ( raw document ): </h6>
                <button type="button" id="upload_html_file" name="upload_html_file">HTML file</button>
                <input type="file" id="file_upload" style="display : none">
                <div id='file_num'></div>
                <input type="hidden" id="passphraseCreate" value="<?= $_SESSION['passphrase'] ?>">
            </div>
            <div class="row" >
            <h7>Add fund to your account before you create your asset</h7>
        <button type="button" id='CreateAsset'>
         Create Asset
        </button>
        <button type="button" id='addFund' onclick="window.open('https://bank.testnet.algorand.network/')">
         Add Fund
        </button>
        </div>
    </form>
    <div id="demo"></div>
        <div id="result_asset"></div>
        </div>
</main>

<?php require 'foot.php' ?>
</body>
</html>