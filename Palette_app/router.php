<!-- Simple router program for local server for debugging -->

<?php
    if (preg_match('/\.(?:png|jpg|jpeg|gif)$/', $_SERVER["REQUEST_URI"])) {
        return false;    // serve the requested resource as-is.
    } else { 
        require_once('resolver.php');
    }
?>