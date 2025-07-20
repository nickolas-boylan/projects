<?php
    session_start();
?>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coluux | Color Palette Generator</title>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.3.js" integrity="sha256-nQLuAZGRRcILA+6dMBOvcRh5Pe310sBpanc6+QBmyVM=" crossorigin="anonymous"></script>
    <script>
        window.onload = function() {
            var errText = $("#error_text");
            var savText = $("#save_text");

            // Validate Palette Name
            window.validate = function validate() {
                var pal_name = $("#palette-name").val();
                if (pal_name == "") {
                    errText.text("Insert a name before saving your palette");
                    showPopup();
                } else if (pal_name.includes("\\")) {
                    errText.text("Names can't contain a backslash");
                    showPopup();
                } else {
                    savePal();
                }
            }

            function savePal() {
                var pal_name = $("#palette-name").val();
                var color0 = $("#color0").val();
                var color1 = $("#color1").val();
                var color2 = $("#color2").val();
                var color3 = $("#color3").val();
                var color4 = $("#color4").val();

                // Run the AJAX request to the save.php file
                $.ajax({
                    url : "save.php",
                    method : "GET",
                    data: {name: pal_name, type: "norm", color0: color0, color1: color1, color2: color2, color3: color3, color4: color4},
                    success: function(result) {
                        // Check Save status
                        if (result == "logged") {
                            errText.html("You must be logged in to save a palette");
                            showPopup();
                        } else if (result == "repeat") {
                            errText.html("Palette names must be unique");
                            showPopup();
                        } else if (result == "max") {
                            errText.html("You have reached the maximum number of palettes you can save with a free account.<br/>To save more palettes, signup for Coluux+");
                            showPopup();
                        } else if (result == "saved") {
                            showSave();
                        } else {
                            errText.html(result);
                            showPopup();
                        }
                    },
                    error: function(xhr) {
                        console.log(xhr.status + " " + xhr.statusText)
                    }
                });
            }

            function showPopup() {
                $("#popup").css("display", "flex");
                $("#shade").show();
            }

            function showSave() {
                popup = $("#save_popup");
                popup.css("display", "flex");
                $("#shade").show();

                setTimeout(function() {
                    popup.fadeOut();
                    $("#shade").fadeOut();
                    $("#palette-name").val("");
                }, 1000);
            }

            window.closePopup = function closePopup() {
                $("#popup").hide();
                $("#shade").hide();
            }

            window.logout = function logout() {
                $.ajax({
                    url : "logout.php", // TODO: Reimplement login/logout
                    success: setTimeout(function() {window.location.replace("index.php")}, 100),
                    error: function(xhr) {
                        console.log(xhr.status + " " + xhr.statusText)
                    }
                });
            }
        }
    </script>
    <link rel="stylesheet" href="nav.css">
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="popup.css">
</head>

<body>
    <div class="shade" id='shade'></div>
    <div class="popup" id="popup">
        <img class="logo" src="coluux_red.png" alt="" id="popup_logo">
        <p id="error_text" class='error_text'></p>
        <button id="back" class="button" onclick="closePopup()">
            Go Back
        </button>
    </div>
    <div class="popup" id="save_popup">
        <p id="save_text" class='error_text'>Palette has been saved</p>
    </div>
    <div class="main-container">
        <div class="nav">
            <div class="nav-top">
                <a href='index.php'><img class="logo" src="coluux_red.png" alt="" style="display: block; margin: auto;"></a>
                <div class="links-container">
                    <a href="" class="nav-link current">
                        <svg width="20" height="21" viewBox="0 0 20 21" fill="none" xmlns="http://www.w3.org/2000/svg"
                            class="nav-link-icon">
                            <path
                                d="M18.6121 8.38446C18.5245 8.63031 18.3884 8.85608 18.2119 9.04839C18.0355 9.2407 17.8223 9.39572 17.5849 9.5042C16.3213 10.0698 15.2478 10.9881 14.4934 12.1489C13.739 13.3098 13.3357 14.6636 13.3319 16.048C13.3334 16.5309 13.3816 17.0125 13.4757 17.4862C13.5385 17.7757 13.5426 18.0748 13.4879 18.366C13.4332 18.657 13.3208 18.9343 13.1573 19.1812C13.0189 19.3974 12.8369 19.5822 12.6228 19.7237C12.4087 19.8652 12.1673 19.9604 11.9143 20.0031C11.3655 20.1062 10.8084 20.1578 10.25 20.1571C9.01135 20.1578 7.78509 19.9094 6.6442 19.4268C5.50331 18.9443 4.47101 18.2376 3.6086 17.3482C2.74621 16.459 2.07129 15.4056 1.62395 14.2505C1.1766 13.0953 0.965941 11.862 1.00447 10.6239C1.0842 8.31542 2.02047 6.11924 3.63086 4.46327C5.24127 2.8073 7.41045 1.81012 9.71586 1.66602H10.2398C11.9612 1.66645 13.6484 2.14749 15.1113 3.05498C16.5741 3.96245 17.7546 5.26033 18.5197 6.80244C18.7551 7.29038 18.7884 7.8516 18.6121 8.36391V8.38446Z"
                                stroke="#555555" stroke-width="1.39926" />
                            <path d="M5.76074 15.0295L5.77062 15.0186" stroke="#555555" stroke-width="1.39926"
                                stroke-linecap="round" stroke-linejoin="round" />
                            <path d="M3.70605 10.9211L3.71593 10.9102" stroke="#555555" stroke-width="1.39926"
                                stroke-linecap="round" stroke-linejoin="round" />
                            <path d="M5.76074 6.81273L5.77062 6.80176" stroke="#555555" stroke-width="1.39926"
                                stroke-linecap="round" stroke-linejoin="round" />
                            <path d="M9.86914 4.75804L9.87902 4.74707" stroke="#555555" stroke-width="1.39926"
                                stroke-linecap="round" stroke-linejoin="round" />
                            <path d="M13.9795 6.81273L13.9894 6.80176" stroke="#555555" stroke-width="1.39926"
                                stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                        <p class="nav-link-lable">Palette Generator</p>
                    </a>
                    <a href="ui.php" class="nav-link">
                        <svg class="nav-link-icon" width="19" height="19" viewBox="0 0 19 19" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M1 12.3461V1.38109C1 1.09943 1.22834 0.871094 1.51 0.871094H17.49C17.7717 0.871094 18 1.09943 18 1.38109V12.3461M1 12.3461V13.9611C1 14.2428 1.22834 14.4711 1.51 14.4711H17.49C17.7717 14.4711 18 14.2428 18 13.9611V12.3461M1 12.3461H18M6.95 17.8711H8.225M8.225 17.8711V14.4711M8.225 17.8711H10.775M10.775 17.8711H12.05M10.775 17.8711V14.4711"
                                stroke="#555555" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                        <p class="nav-link-lable">UI Palette Generator</p>
                    </a>
                    <a href="browse.php" class="nav-link">
                        <svg class="nav-link-icon" width="19" height="20" viewBox="0 0 19 20" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M5.79274 18.6708H17.6787C17.9964 18.6708 18.2538 18.4134 18.2538 18.0957V1.99212C18.2538 1.67449 17.9964 1.41699 17.6787 1.41699H1.57513C1.25749 1.41699 1 1.67449 1 1.99212V13.8781"
                                stroke="#555555" stroke-width="1.39636" stroke-linecap="round"
                                stroke-linejoin="round" />
                            <path d="M7.70996 4.29297H15.3783" stroke="#555555" stroke-width="1.39636"
                                stroke-linecap="round" stroke-linejoin="round" />
                            <path d="M3.87598 4.29297H4.83452" stroke="#555555" stroke-width="1.39636"
                                stroke-linecap="round" stroke-linejoin="round" />
                            <path d="M1.47949 18.1916L9.62714 10.0439M9.62714 10.0439V13.8781M9.62714 10.0439H5.79295"
                                stroke="#555555" stroke-width="1.39636" stroke-linecap="round"
                                stroke-linejoin="round" />
                        </svg>

                        <p class="nav-link-lable">My Palettes</p>
                    </a>
                    <?php
                        if (isset($_SESSION["username"]) && !$_SESSION["premium"]) {
                            echo "<a href='premium.php' class='nav-link'>
                            <svg class='nav-link-icon' width='19' height='20' viewBox='0 0 19 20' fill='none'
                                xmlns='http://www.w3.org/2000/svg'>
                                <path d='M10 2 L10 18 M2 10 L18 10'
                                    stroke='#555555' stroke-width='1.39636' stroke-linecap='round'
                                    stroke-linejoin='round' />
                            </svg>
                            <p class='nav-link-lable'>Subscribe to Coluux+</p>
                        </a>";
                        } else if ($_SESSION["premium"]) {
                            echo "<a href='unsubscribe.php' class='nav-link'>
                            <svg class='nav-link-icon' width='19' height='20' viewBox='0 0 19 20' fill='none'
                                xmlns='http://www.w3.org/2000/svg'>
                                <path d='M10 2 L10 18 M2 10 L18 10'
                                    stroke='#555555' stroke-width='1.39636' stroke-linecap='round'
                                    stroke-linejoin='round' />
                            </svg>
                            <p class='nav-link-lable'>Unsubscribe</p>
                        </a>";
                        }
                    ?>
                </div>
            </div>
            <div class="nav-bottom">
                <?php
                    // Add either login button or account info
                    // TODO: Implement proper authentication and replace session ids
                    if (!isset($_SESSION["username"])) {
                        echo "<div class='login-left'><a href='login.php' class='button'><p>Login</p></a></div>";
                    } else {
                        echo "<button type='button' class='button' id='logoutButton' onclick='logout()'>Logout</button>";
                    }
                ?>
            </div>
        </div>

        <div class="body-container">
            <div class="body-top">
                <div class="body-top-left">
                    <svg class="pencil-icon" width="22" height="22" viewBox="0 0 20 20" fill="none"
                        xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M10.7171 4.03706L13.4934 1.26074L18.3519 6.11929L15.5756 8.89556M10.7171 4.03706L1.28749 13.4667C1.10342 13.6507 1 13.9004 1 14.1607V18.6127H5.45196C5.71229 18.6127 5.96196 18.5093 6.14604 18.3252L15.5756 8.89556M10.7171 4.03706L15.5756 8.89556"
                            stroke="#555555" stroke-width="1.30139" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>

                    <input type="text" id="palette-name" name="palette-name" placeholder="Untitled Palette">
                </div>
                <div class="body-top-right">
                    <button type="button" class="button save" onclick="validate()">
                        <svg viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M1 12.9351V2.48164C1 1.65688 1.6686 0.988281 2.49335 0.988281H10.8349C11.231 0.988281 11.6108 1.14561 11.8909 1.42568L14.0028 3.53759C14.2829 3.81766 14.4402 4.19749 14.4402 4.59356V12.9351C14.4402 13.7599 13.7716 14.4285 12.9468 14.4285H2.49335C1.6686 14.4285 1 13.7599 1 12.9351Z"
                                stroke="#F92B67" stroke-width="0.887608" />
                            <path
                                d="M5.18238 5.46834H10.2598C10.5072 5.46834 10.7078 5.26776 10.7078 5.02034V1.43629C10.7078 1.18886 10.5072 0.988281 10.2598 0.988281H5.18238C4.93496 0.988281 4.73438 1.18886 4.73438 1.43629V5.02034C4.73438 5.26776 4.93496 5.46834 5.18238 5.46834Z"
                                stroke="#F92B67" stroke-width="0.887608" />
                            <path
                                d="M3.24023 8.90308V14.4285H12.2004V8.90308C12.2004 8.65564 11.9998 8.45508 11.7524 8.45508H3.68824C3.44081 8.45508 3.24023 8.65564 3.24023 8.90308Z"
                                stroke="#F92B67" stroke-width="0.887608" />
                        </svg>
                        <p>Save Palette</p>
                    </button>
                    <a href="" class="button">
                        <p>New Palette</p>
                        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <line x1="6.54927" y1="0.786133" x2="6.54927" y2="12.325" stroke="white"
                                stroke-width="0.887608" />
                            <line x1="0.720703" y1="6.49663" x2="12.2596" y2="6.49663" stroke="white"
                                stroke-width="0.887608" />
                        </svg>
                    </a>
                </div>
            </div>

            <div class="tool-container">
                <div class="tool-col left">
                    <button type='button' onclick="randomizePalette()" class="button">
                        <p>Randomize</p>
                    </button>
                    <div class="loader"></div>
                </div>
            </div>

            <div class="color-palette-container" id="palette-container">
                <!-- <div class="color-container">
                    <div class="lock-container">
                        <p>Lock</p>
                        <input type="checkbox" id="lock">
                    </div>
                    <input type="color" class="color" id="color" value="#0000ff">
                    <div class="color-info">
                        <div class="color-info-row">
                            <p class="info-key">RGB</p>
                            <p class="info-value" id="rgb">12, 12, 12</p>
                        </div>
                        <div class="color-info-row">
                            <p class="info-key">HEX</p>
                            <p class="info-value" id="hex">#121212</p>
                        </div>
                    </div>
                </div> -->
            </div>
        </div>
    </div>
    <script src="darkmode.js"></script>
    <script src="script.js"></script>
</body>

</html>