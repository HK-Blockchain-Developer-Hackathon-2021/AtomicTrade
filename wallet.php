<?php
    require 'check_login_status.php';
?>
<html>

<?php require 'head.php'?>

<script src="check.js"></script>
<head>
<link rel="stylesheet" href="style.css">

</head>
<body>
<?php require 'header.php'?>
    <main>
    container ! index page 
        <?= ( "<h4>Welcome ! Address : " . $_SESSION['user'] ."</h4>" );?>
        <h6>You can click any one of the following button to use the functions</h6>
        <button id='transaction' onclick="location.href='document_transfer.php'">Transaction</button>
        <button id='CheckID' onclick="location.href='document_opt_in.php'" >Opt-in Documents</button>
        <button id='VerifyDocumet' onclick="location.href='verify_document.php'">Verify Document</button>
        <button id='CreateDocumet' onclick="location.href='document_create.php'">Create Document</button>
        <div id="a"></div>


        account index show balance / xxxx

        

        
        <div class="tab" id="tab-2">
      <label for="name">Transaction ID:</label>
      <input type="text" id="txid" name="txid" required maxlength="255" size="150">
      <button type="button" id='transaction'>
         Check Transaction
        </button>
      </div>
    
      </main>
      <?php require 'foot.php' ?>
</body>

</html>