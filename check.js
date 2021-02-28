/*

//sandbox
const algodToken = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const algodServer = "http://localhost";
const algodPort = 4001;
// init a client
let algodClient = new algosdk.Algodv2(algodToken, algodServer, algodPort);*/

console.log("aa");

var passphrase;
var account;
var html_code;

// for index part
$('#access').click(function() {
    console.log("ab");
    // run algorand stuff now --> check the passphrase vs address is same/not
    passphrase = $('#passphrase').val(); //maybe logn [input id=...]
    account = "";
    try {
        account = algosdk.mnemonicToSecretKey(passphrase);
        $.ajax({
            type: "POST",
            async: false,
            url: "authentication.php",
            data: {
                "address": account.addr,
                "passphrase": passphrase
            },
            success: function(data) {
                console.log(data);
                console.log("success");
                window.location.replace("wallet.php"); // change 
            },
            error: function(data) {
                console.log("error");
                console.log(data);
            },
        });
    } catch (err) {
        document.getElementById('validate').innerHTML = " <span class='reminder'> Please enter the correct passphrase. </span> ";

    }
    //if there's no error then pass to authetication 

    // ajax to authentication.php post , address

});

$('#create').click(function() {
    // genereate a key-value pair 

    account = algosdk.generateAccount();
    passphrase = algosdk.secretKeyToMnemonic(account.sk);
    document.getElementById("info").innerHTML =
        "Your address would be : <b>" + account.addr +
        "</b> <br><br>Your passphrase would be : <br><b>" + passphrase +
        "</b> <br><br> <span class='reminder'> * Important * </span><br>please be reminded that address ......<br>";
    // add copy to cliboard function
    $('#change').show();
    // display message about address & passphrase on the above info

})

$('#change').click(function() {
            $.ajax({
                type: "POST",
                async: false,
                url: "authentication.php",
                data: {
                    "address": account.addr,
                    "passphrase": passphrase
                },
                success: function(data) {
                    console.log(data);
                    console.log("success");
                    window.location.replace("wallet.php"); // change 
                },
                error: function(data) {
                    console.log("error");
                    console.log(data);
                },
            });
        }

    )
    //---------------------- index page over ---------------------------------------------------------------------
    //------------------------- wallet page ----------------------------------------------------

//logout---------------------------------------------------
$('#logout').click(() => {
    window.location.replace("authentication.php?action=logout");
})

//Create Asset -------------------------------------------------------------------
function onChange(event) {
    document.getElementById('file_num').innerHTML = " You have uploaded 1 file.";

    var file_data = $('#file_upload').prop('files')[0];
    var form_data = new FormData();
    form_data.append('file', file_data);
    $.ajax({
        url: '../Algorand-Blockchain-Hackathon-2021/program/web_scrap.php', // point to server-side PHP script 
        dataType: 'text', // what to expect back from the PHP script, if anything
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,
        type: "POST",
        success: function(php_script_response) {
            html_code = php_script_response; // display response from the PHP script, if any
            console.log(html_code);
            //document.getElementById("demo").innerHTML = html_code;
        }
    });
}



$('#upload_html_file').click(() => {
    $('#file_upload').trigger('click');
    // enable select file function
    // turn the file into html code
    // store in the 
    document.getElementById('file_upload').addEventListener('change', onChange);
})

$('#CreateAsset').click(() => {
        // validate check first , if yes then , no then validate!!!!!!!!
        let pass_python = {
            "method": "create",
            "hashed-doc": html_code,
            "doc-id": $('#doc-id').val(),
            "doc-name": $('#doc-name').val(),
            "passphrase": $('#passphraseCreate').val()
        };
        console.log(html_code);

        pass_python = JSON.stringify(pass_python);

        console.log("html 2 " + pass_python);
        $.ajax({
            type: "POST",
            async: false,
            url: "../Algorand-Blockchain-Hackathon-2021/program/run_python.php",
            data: {
                "data": pass_python
            },
            success: function(data) {
                console.log("Asset create with id : " + data);
                document.getElementById("result_asset").innerHTML =
                    "Congrat! You have successfully create the Asset : " + $('#doc-id').val() +
                    "<br> <span class='reminder'>The Asset-ID is " + data + "</span> ";
            },
            error(data) {
                document.getElementById("result_asset").innerHTML =
                    "Sorry! There is an error occured <br>The Asset : " + $('#doc-id').val() + " is not created! ";
            }
        })
    })
    //-----opt-in---------------------------------------------------------------------------------------
$('#sign-opt-in').click(() => {

    let pass_python = {
        "method": "opt-in",
        "asset-id": $('#asset-ID-opt-in').val(),
        "passphrase": $('#passphrase-opt-in').val()
    };
    pass_python = JSON.stringify(pass_python);

    console.log("opt-in");
    $.ajax({
        type: "POST",
        async: false,
        url: "../Algorand-Blockchain-Hackathon-2021/program/run_python.php",
        data: {
            "data": pass_python
        },
        success: function(data) {
            console.log("opt-in data passed : " + data);
            document.getElementById("result_opt-in").innerHTML =
                "<span class='reminder'>Congrat! You have successfully opt-in the Asset : " + $('#asset-ID-opt-in').val() + "</span>";
        },
        error(data) {
            document.getElementById("result_opt-in").innerHTML =
                "Sorry! There is an error occured ~ Fail to opt-in the Asset-ID : " + $('#asset-ID-opt-in').val() + " ! ";
        }
    })


})

// trasfer-----------------------------------------------------------------
$('#sign-transfer').click(() => {

    let pass_python = {
        "method": "transfer",
        "asset-id": $('#asset-ID-transfer').val(),
        "passphrase": $('#passphrase-transfer').val(),
        "other_public_key": $('#public-key-other').val()
    };
    pass_python = JSON.stringify(pass_python);

    console.log("transfer");
    $.ajax({
        type: "POST",
        async: false,
        url: "../Algorand-Blockchain-Hackathon-2021/program/run_python.php",
        data: {
            "data": pass_python
        },
        success: function(data) {
            console.log("transfer data passed : " + data);
            document.getElementById("result_transfer").innerHTML =
                "<span class='reminder'>Congrat! You have successfully transfer the Asset : " + $('#asset-ID-transfer').val() + "</span>";
        },
        error(data) {
            document.getElementById("result_transfer").innerHTML =
                "Sorry! There is an error occured ~ Fail to transfer the Asset-ID : " + $('#asset-ID-transfer').val() + " ! ";
        }
    })


})

// verify -----
function onChange2(event) {
    document.getElementById('file_num').innerHTML = " You have uploaded 1 file.";

    var file_data = $('#file_upload_verify').prop('files')[0];
    var form_data = new FormData();
    form_data.append('file', file_data);
    $.ajax({
        url: '../Algorand-Blockchain-Hackathon-2021/program/web_scrap.php', // point to server-side PHP script 
        dataType: 'text', // what to expect back from the PHP script, if anything
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,
        type: "POST",
        success: function(php_script_response) {
            html_code = php_script_response; // display response from the PHP script, if any
            console.log(html_code);
            //document.getElementById("demo").innerHTML = html_code;
        }
    });
}
$('#upload_html_file_verify').click(() => {
    $('#file_upload_verify').trigger('click');
    // enable select file function
    // turn the file into html code
    // store in the 
    document.getElementById('file_upload_verify').addEventListener('change', onChange2);
})
$('#verify').click(() => {
    // validate check first , if yes then , no then validate!!!!!!!!
    let pass_python = {
        "method": "verify",
        "hashed-doc": html_code,
        "doc-name": $('#doc-name-verify').val(),
        "pk": $('#pk').val()
    };

    console.log(html_code);

    pass_python = JSON.stringify(pass_python);

    console.log("html 2 " + pass_python);
    $.ajax({
        type: "POST",
        async: false,
        url: "../Algorand-Blockchain-Hackathon-2021/program/run_python.php",
        data: {
            "data": pass_python
        },
        success: function(data) {
            console.log("Asset create with id : " + data);
            document.getElementById("result_asset").innerHTML = data;
        },
        error(data) {
            document.getElementById("result_asset").innerHTML =
                "Sorry! There is an error occured <br>The Asset : " + $('#doc-id').val() + " is not created! ";
        }
    })
})