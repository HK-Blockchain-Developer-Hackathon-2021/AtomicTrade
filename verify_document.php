<html>

<?php require 'head.php'?>

<body>
<main>
<?php require 'header.php'?>
<div class="row">
                <label for="doc-name">Document Name :</label>
                <input type="text" id="doc-name-verify" name="doc-name-verify" required size="70">
            </div>
    
            <div class="row">
    <label for="pk">The owner's public key</label>
    <input type = "text" id="pk" name="pk" required>
    </div>
    <div class="row">
        <h6>You can verify a document to see if it is exist on the block !</h6>
        <h6>Please upload your HTML file ( raw document ): </h6>
        <button type="button" id="upload_html_file_verify" name="upload_html_file_verify">HTML file</button>
        <input type="file" id="file_upload_verify" style="display : none">
        <div id='file_num'></div>
          
    </div>
    <div class="row">
    <button type="button" id="verify" name="verify">
    Verify Documet</button>
    </div>

    <div class="row">
    <div id='result_asset'></div>
    </div>
</main>

<?php require 'foot.php' ?>
</body>
</html>