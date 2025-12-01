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
            numButtons = parseInt($("#numButtons").val());
            for (i = 0; i < numButtons; i++) {
                let id = "#button" + i;
                let conId = "#container" + i;
                $(id).on("click", function() {
                    deletePal($(id).val());
                    $(conId).fadeOut();
                });
            }

            function deletePal(name) {
                $.ajax({
                    url : "delete.php",
                    method : "GET",
                    data: {name: name},
                    error: function(xhr) {
                        console.log(xhr.status + " " + xhr.statusText)
                    }
                });
            }

            window.logout = function logout() {
                $.ajax({
                    url : "logout.php",
                    success: setTimeout(function() {window.location.replace("browse.php")}, 100),
                    error: function(xhr) {
                        console.log(xhr.status + " " + xhr.statusText)
                    }
                });
            }
        }
    </script>
    <link rel="stylesheet" href="nav.css">
    <link rel="stylesheet" href="browse.css">
    <style type="text/css">
        .deleteButton {
            display: none;
            background-color: inherit;
            border: none;    
        }

        .deleteButton:hover {
            cursor: pointer;
        }

        .color-container:hover .deleteButton {
            display: unset;
        }

        .color-info-row {
            align-items: center;
        }

        .trash {
            height: 35px;
        }

        .color {
            display: flex;
            height: auto;
        }

        .hoverColor {
            display: none;
            margin: auto;
            background-color: rgba(255, 255, 255, 0.3);
            border: transparent 2px solid;
            border-radius: 10px;
            padding: 3px;
        }

        .color:hover .hoverColor {
            display: inline-block;
        }

        form {
            display: flex;
            flex-direction: row;
            height: 100%;
            width: 100%;
        }

        @media (max-width: 1080px) {
            div.color {
                width: 55%;
            }

            .color-info {
                display: flex;
                text-align: center;
            }

            .deleteButton {
                margin-top: 20px;
            }
        }
    </style>
</head>

<body>
    <div class="main-container">
        <form method='post' action='delete.php'>
        <div class="nav">
            <div class="nav-top">
                <a href='index.php'><img class="logo" src="coluux_red.png" alt="" style="display: block; margin: auto;"></a>
                <div class="links-container">
                    <a href="index.php" class="nav-link ">
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
                    <a href="" class="nav-link current">
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
                        // TODO: Redo session ids to make more secure authenticators
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
                    <p id="palette-name">My Palettes</p>
                </div>
                <div class="body-top-right">
                    <a href="index.php" class="button">
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

            <div class="color-palette-container" id="palette-container">
                <?php
                    // based on original work from the PHP Laravel framework
                    // Function available in future editions of PHP
                    if (!function_exists('str_contains')) {
                        function str_contains($haystack, $needle) {
                            return $needle !== '' && mb_strpos($haystack, $needle) !== false;
                        }
                    }

                    // Function to take the name of a palette and process it
                    // Needed for names with " or $ within them
                    function processString($input) {
                        if (str_contains($input, '"')) {
                            $split = explode('"', $input);
                            $input = "";
                            
                            // Put together the split up one with the transformed char
                            for ($i = 0; $i < sizeof($split); $i++) {
                                $input .= $split[$i];
                                if ($i != sizeof($split) - 1) {
                                    $input .= '\"';
                                }
                            }
                        }

                        // Now check for $
                        if (str_contains($input, "$")) {
                            $split = explode("$", $input);
                            $input = "";
                            
                            // Put together the split up one with the transformed char
                            for ($i = 0; $i < sizeof($split); $i++) {
                                $input .= $split[$i];
                                if ($i != sizeof($split) - 1) {
                                    $input .= "$";
                                }
                            }
                        }

                        return $input;
                    }

                    // Function to make the overall color container
                    function makeContainer($i) {
                        $div = "<div class='color-container' id='container$i'> <div class = 'palette-color-container'>";

                        return $div;
                    }

                    // Function to make each individual color in the palette
                    function makePalette($c1, $c2, $c3, $c4, $c5="") {
                        $palette = "<div class='color' style='background-color: $c1;'><div class='hoverColor'>$c1</div></div><div class='color' style='background-color: $c2;'><div class='hoverColor'>$c2</div></div><div class='color' style='background-color: $c3;'><div class='hoverColor'>$c3</div></div><div class='color' style='background-color: $c4;'><div class='hoverColor'>$c4</div></div>";

                        // Check if ui theme is being made or normal
                        if ($c5 != "") {
                            $palette .= "<div class='color' style='background-color: $c5;'><div class='hoverColor'>$c5</div></div></div>";
                        } else {
                            $palette .= "</div>";
                        }

                        return $palette;
                    }

                    // Function to add the color's info (name) to the bottom
                    // Also adds a delete button
                    function makeInfo($name, $id) {
                        $palInfo = "<div class='color-info'><div class='color-info-row'><p class='info-key'>$name</p><button type='button' class='deleteButton' id='button$id' value=\"$name\"><img src='trash.png' class='trash'></button></div></div></div>";

                        return $palInfo;
                    }

                    // Check if the user is signed in first
                    if (! isset($_SESSION["username"])) {
                        // Not signed in
                        echo "<div class='error_box' id='error_box'> You must be signed in to browse saved palettes.</div>";
                    } else {
                        // Connect to server
                        $servername = "localhost";
                        $user = "usbarelzt5gqe";
                        $pw = "TuftsCS20";
                        $db = new mysqli($servername, $user, $pw);

                        // Check connection
                        if ($db->connect_error) {
                            die("Connection to Server Failed");
                        }

                        // Select Database
                        $db->select_db("dbvzfq2glyjk1h");
                        $name = $_SESSION["username"];

                        // Make and send query
                        $query = "SELECT * FROM palettes INNER JOIN users ON palettes.user_id = users.user_id WHERE username = '$name'";
                        $result = $db->query($query);
                        
                        // Check for result and go through returned table
                        if ($result->num_rows > 0) {
                            $i = 0;
                            while ($row = $result->fetch_assoc()) {
                                $newDiv = makeContainer($i);
                                $newDiv .= makePalette($row["color1"], $row["color2"], $row["color3"], $row["color4"], $row["color5"]);
                                $newDiv .= makeInfo(processString($row["palette_name"]), $i);
                                echo $newDiv;
                                $i++;
                            }

                            echo "<input type='hidden' id='numButtons' value='$i'>";
                        } else {
                            echo "No palettes saved!<br/>";
                        }

                        // Close connection
                        $db->close();
                    }
                ?>
            <input type='hidden' id='nameToDelete' name='nameToDelete'>
        </div>
        </form>
    </div>
    <script src="darkmode.js"></script>
</body>

</html>