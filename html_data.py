html_data = '''
<html>
    <head>
    <meta charset="utf-8" />
    <style>
        body {{
            display: block;
            width: 100%;
            text-align: center;
        }}
        #chart_div {{
            display: block;
            width: 95%;
            height: 95%;
            padding-top: 0px;
            margin: -60px auto 0;
        }}
        .buttonsWrapper {{
            display: block;
        }}
        .butt {{
            margin-right: 3px;
            display: inline-block;
            min-width: 50px;
            height: 35px;
            background: #dad9d9;
            padding: 3px 5px 5px 3px;
            text-align: center;
            border-radius: 5px;
            // font-weight: bold;
            cursor: pointer;
            color: #444;          
        }}
        
        .inactive {{
            background: #d4d4d4;
            color: #776767;
            border: 3px solid #d4d4d4;
            text-decoration: line-through;
        }}
        .buttons {{
            margin-left: 50px;
            display: inline-block;
        }}
        .dateInput {{
            display: block;
            align-items: center;
            width: min-content;
            margin: 0 auto 50px;
        }}
        
        input[type=submit] {{
            padding:5px 15px; 
            background:#ccc; 
            border:0 none;
            cursor:pointer;
            -webkit-border-radius: 5px;
            border-radius: 5px; 
        }}
        
        label {{
          display: inline-block;
          width: 300px;
        }}
        
        input:invalid+span:after {{
            content: '✖';
            padding-left: 5px;
        }}
        
        input:valid+span:after {{
            content: '✓';
            padding-left: 5px;
        }}
    </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
        <!-- Compiled and minified JavaScript -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            var datefield=document.createElement("input");
            datefield.setAttribute("type", "date");
            if (datefield.type != "date") {{ //if browser doesn't support input type="date", load files for jQuery UI Date Picker
                document.write('<link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css" />')
                document.write('<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"><\/script>')
                document.write('<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"><\/script>') 
            }}
        </script>
        <script>
            if (datefield.type!="date"){{ //if browser doesn't support input type="date", initialize date picker widget:
                jQuery(function($){{ //on document.ready
                    $('#grafikDate').datepicker({{
                        dateFormat: "yy-mm-dd",
                        minDate: new Date(2018, 11, 11)
                    }});
                }})
            }}
        </script>
        <script type="text/javascript">
        google.charts.load('current', {{'packages':['corechart']}});
        google.charts.setOnLoadCallback(drawAxisTickColors);
        function drawAxisTickColors() {{
            var data = new google.visualization.arrayToDataTable(
        
            {chart_data}
        
            );
                        
            mappingTmp = {{
                1: 'Tkol',
                10: 'Tbat',
                2: 'Tniz',
                3: 'Tyl',
                4: 'dT',
                5: 'STns',
                6: 'STnag',
                7: 'Tkom',
                8: 'Tkol2',
                9: 'Tyst'                
            }};
            
            const dataHeaders = {data_headers}

            const grafiki = {{
                'Tkol': {{id: 1, hiddenState: false, color: 'black'}},                
                'Tniz': {{id: 2, hiddenState: false, color: 'red'}},
                'Tyl': {{id: 3, hiddenState: false, color: 'green'}},
                'dT': {{id: 4, hiddenState: false, color: 'blue'}},
                'STns': {{id: 5, hiddenState: false, color: 'magenta'}},
                'STnag': {{id: 6, hiddenState: false, color: 'grey'}},
                'Tkom': {{id: 7, hiddenState: false, color: 'orange'}},
                'Tkol2': {{id: 8, hiddenState: false, color: 'brown'}},
                'Tyst': {{id: 9, hiddenState: false, color: 'deepskyblue'}},
                'Tbat': {{id: 10, hiddenState: false, color: 'indigo'}},           
            }};
        
            var fillcolors = function () {{
                var colors = []
                for (var i = 0; i < Object.keys(grafiki).length; i++) {{
                    if (!grafiki[Object.keys(grafiki)[i]].hiddenState) {{
                        colors.push(grafiki[Object.keys(grafiki)[i]].color);
                    }}
                }}
                return colors
            }}
        
            var options = {{title: '{grafic_date}',
                colors: fillcolors(),
                legend: {{ position: 'bottom' }}
            }};
                
            var view = new google.visualization.DataView(data);
            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            console.log('INIT COLS : ', view.getViewColumns())            
            
            var initial_draw = function () {{
                 for (let i = 1; i < dataHeaders.length; i++) {{
                    let dName = dataHeaders[i]
                    console.log("DataHeaders: ", dName)
                    console.log("setting button styles: ", grafiki[dName], grafiki[dName]["color"])
                    // document.getElementById(dName).className = ("butt");
                    // document.getElementById(dName).style.border = "3px solid " + grafiki[dName]["color"];
                    html_to_insert = '<a onclick=toggleGrafik("'
                    html_to_insert += dName + '") '
                    html_to_insert += 'class="butt" style="border: 3px solid ' + grafiki[dName]["color"] + '" id="' + dName + '"'
                    html_to_insert += \">" + dName + "</a>"
                    console.log("html_to_insert: ", html_to_insert)
                    document.getElementById("buttons").insertAdjacentHTML("beforeend", html_to_insert);
                }}
            }}
            
            allOff = function () {{
                for (let i = 1; i < dataHeaders.length; i++) {{                    
                    let dName = dataHeaders[i]
                    console.log(dName)
                    view.hideColumns([grafiki[dName].id])
                    grafiki[dName].hiddenState = true
                    document.getElementById(dName).className = ("butt inactive");
                    document.getElementById(dName).removeAttribute('style');
                    console.log('AFTER HIDE ALL : ', view.getViewColumns())
                }}
                options.colors = fillcolors()
                chart.draw(view, options);
                console.log("Off")
                chart.clearChart()
            }}        
            
            toggleGrafik = function(grafikName) {{
                grafiki[grafikName].hiddenState = !grafiki[grafikName].hiddenState 
                if (grafiki[grafikName].hiddenState) {{ 
                    view.hideColumns([grafiki[grafikName].id])
                    document.getElementById(grafikName).className = ("butt inactive");
                    document.getElementById(grafikName).removeAttribute('style');
                    
                }}
                else {{
                    var restore = view.getViewColumns()
                    console.log('getViewColumns', restore)
                    console.log('getViewColumnsSorted', restore.sort((a, b) => a - b))
                    restore.push(grafiki[grafikName].id)
                    view.setColumns(restore.sort((a, b) => a - b))
                    document.getElementById(grafikName).className = ("butt");
                    document.getElementById(grafikName).style.border = "3px solid " + grafiki[grafikName]["color"];
                }}
                options.colors = fillcolors()
                console.log('Options colors : ', options.colors)
                chart.draw(view, options);
                console.log('AFTER REDRAW : ', view.getViewColumns()) 
            }}

            function selectHandler(e) {{
                var selection = chart.getSelection()
                //alert('The user selected' + selection[0].column + ' items.')
                console.log(selection[0].column, mappingTmp[selection[0].column])
                toggleGrafik(mappingTmp[selection[0].column])
            }}

            google.visualization.events.addListener(chart, 'select', selectHandler);
            chart.draw(view, options);
            initial_draw()
            console.log('SERIES START: ', options.colors);    
        }}
        </script>
    </head>
    <body>
        <div id="top">
            
            <div id="chart_div" class="chart">
            </div>
            <div id="APIErrorMessage" style="width: 900px; margin: auto; text-align: center; color: red">
            </div>
            <div id="dataUpdateErrorMessage" style="width: 900px; margin: auto; text-align: center; color: red">
            </div>
            <div class="buttonsWrapper">
                <div id="buttons" class="buttons">                
                </div>
                <div id="nasos_nagrev" style="display: inline-block">                
                    <a class="waves-effect waves-light btn-small grey" id="nasos">Насос</a>
                    <a class="waves-effect waves-light btn-small grey" id="nagrev">Нагрев</a>
                    <a onclick=allOff() class="waves-effect waves-light btn-small grey" id="all_off">Выкл гр</a>                    
                </div>
            </div>
            <div style="width: 900px; margin: auto"; text-align: left;">
                <h5>Архив данных: </h5>
                    <form class="dateInput" id="dateInput">
                        <b>Выбрать дату:</b>
                        <input type="date" id="grafikDate" name="date" size="20" min="2018-12-11"/>
                        <input type="submit" value="Выбрать"></p>
                    </form>
            </div>
        </div>
    </body>
    <script>
    
        const dataHeaders = {data_headers}        
        var status_nasos_nagrev = {status_nasos_nagrev}
        var status_nasos = status_nasos_nagrev.status_relay.status_nasos 
        var status_nagrev = status_nasos_nagrev.status_relay.status_nagrev
        var nasos = document.getElementById("nasos");
        var nagrev = document.getElementById("nagrev");
        var APIErrorMessage = document.getElementById("APIErrorMessage");
        var dataUpdateErrorMessage = document.getElementById("dataUpdateErrorMessage");   
        
        grafikDate.setAttribute("max", new Date().toISOString().split("T")[0]);
        grafikDate.setAttribute("value", new Date().toISOString().split("T")[0]);
        
        nasos.onclick = function() {{
            if (status_nasos === 0) {{path = "/on1"}}
            if (status_nasos === 1) {{path = "/off1"}}
            sendSwitchQuery({{"relayObject": nasos, "relayString": "status_nasos", "relay_state": window.status_nasos, "path": path, "strName": "насос"}})
        }}        
        
        nagrev.onclick = function() {{
            if (status_nagrev === 0) {{path = "/on2"}}
            if (status_nagrev === 1) {{path = "/off2"}}
            sendSwitchQuery({{"relayObject": nagrev, "relayString": "status_nagrev", "relay_state": window.status_nagrev, "path": path, "strName": "нагрев"}})
        }}
        
        sendSwitchQuery = function(reqParam) {{
            var xhr1 = new XMLHttpRequest();
            console.log("requested switch for ", reqParam.relayString, "Path: ", reqParam.path)
            xhr1.open('GET', reqParam.path, true);
            xhr1.send();
            xhr1.onreadystatechange = function() {{ // (3)
                api_resp = {{"code": 0}}
                if (xhr1.responseText != '') {{
                    api_resp = JSON.parse(xhr1.responseText);
                    }}
                console.log('API_RESP: ', api_resp)
                if (xhr1.readyState != 4) return;
                if (xhr1.status != 200 || api_resp.error_code !== 0) {{
                    alert('Ошибка сервера управления: \\n' + api_resp.error);
                }} 
                else {{
                    status_nasos_nagrev.error_code = 0
                    // alert('Переключение реле: ' + reqParam.strName + '\\n' + 
                    // 'Исходный статус: ' + window[reqParam.relayString] + '\\n' +
                    // 'Новый статус: ' + api_resp.status_relay[reqParam.relayString]);
                    console.log(reqParam.relayString, ' before: ', window[reqParam.relayString])
                    window[reqParam.relayString] = api_resp.status_relay[reqParam.relayString] // invert switch state for passed relay_state variable
                    console.log(reqParam.relayString, ' after: ', api_resp.status_relay[reqParam.relayString], '\\nstatus_nasos: ', status_nasos, '\\nstatus_nagrev: ', status_nagrev)
                    if (window[reqParam.relayString] === 0) {{
                        reqParam.relayObject.className = ("waves-effect waves-light btn-small grey");
                    }}
                    if (window[reqParam.relayString] === 1) {{
                        reqParam.relayObject.className = ("waves-effect waves-light btn-small red");
                    }}
                }}
            }}
        }}
        
        if (status_nasos_nagrev.error_code === 1) {{
            APIErrorMessage.innerHTML = ("<h5>Сервер управления насосом/нагревом недоступен</h5>" +
            "<p>" + status_nasos_nagrev.error + "</p>")
        }}
        if (status_nasos_nagrev.error_code === 2) {{
            dataUpdateErrorMessage.innerHTML = ("<h5>Обновление данных в реальном времени недоступно</h5>" +
            "<p>" + status_nasos_nagrev.error + "</p>")
            nagrev.disabled = true;
            nasos.disabled = true;
        }}
        if (status_nasos === 1) {{
            nasos.className = ("waves-effect waves-light btn-small red");
            }}
        if (status_nagrev === 1) {{
            nagrev.className = ("waves-effect waves-light btn-small red");
            }}
    </script
</html>'''