

<html>
<header class="header header-two" style="z-index:10000">
<nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" href="wallet.php">HKU FinTech TEAM</a>
    </div>

    <div class="navbar-menu">
      <div class="navbar-start">
        <a class="navbar-item" href="document_transfer.php">Asset Transaction Tx</a>
        <a class="navbar-item" href="document_create.php">Asset Create Tx</a>
        <a class="navbar-item" href="document_opt_in.php">Asset Opt-in Tx</a>
        <a class="navbar-item" href="verify_document.php">Verify Document </a>

        <?php if (empty($_SESSION['user'])){?>
        <a class="navbar-item" href="index.php">login</a>
          <?php } else{?>
        <a class="navbar-item" href="#" id="logout">Logout</a>
        <?php }?>
        

      </div>

      <div class="navbar-end">
        <a class="navbar-item" target="_blank" rel="noopener noreferrer" href="https://github.com/leehiulong/Algorand-Blockchain-Hackathon-2021">
          Documentation
        </a>
      </div>
    </div>
  </nav>
</main>
</header>
</html>