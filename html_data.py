html_data = '''
<html>
    <head>
    <meta charset="utf-8" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
        <!-- Compiled and minified JavaScript -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
        google.charts.load('current', {{'packages':['corechart']}});
        google.charts.setOnLoadCallback(drawAxisTickColors);
        function drawAxisTickColors() {{
            var data = new google.visualization.arrayToDataTable(
        
            {chart_data}
        
            );
            mappingTmp = {{
                1: 'Tkol',
                2: 'Tniz',
                3: 'Tyl',
                4: 'dT',
                5: 'STns',
                6: 'STnag',
                7: 'Tkom',
                8: 'Tkol2'
            }};

            const grafiki = {{
                'Tkol': {{id: 1, hiddenState: false, color: 'black'}},
                'Tniz': {{id: 2, hiddenState: false, color: 'red'}},
                'Tyl': {{id: 3, hiddenState: false, color: 'green'}},
                'dT': {{id: 4, hiddenState: false, color: 'blue'}},
                'STns': {{id: 5, hiddenState: false, color: 'magenta'}},
                'STnag': {{id: 6, hiddenState: false, color: 'grey'}},
                'Tkom': {{id: 7, hiddenState: false, color: 'orange'}},
                'Tkol2': {{id: 8, hiddenState: false, color: 'brown'}}
            }};
        
            var initialSeries = {{
                0: {{color: 'black', lineWidth: 10, visibleInLegend: true}},
                1: {{color: 'red', lineWidth: 2, visibleInLegend: true}},
                2: {{color: 'green', lineWidth: 2, visibleInLegend: true}},
                3: {{color: 'blue', lineWidth: 2, visibleInLegend: true}},
                4: {{color: 'magenta', lineWidth: 2, visibleInLegend: true}},
                5: {{color: 'grey', lineWidth: 2, visibleInLegend: true}},
                6: {{color: 'orange', lineWidth: 2, visibleInLegend: true}},
                7: {{color: 'brown', lineWidth: 2, visibleInLegend: true}},
                8: {{color: 'cyan', lineWidth: 2, visibleInLegend: true}},
            }}
        
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

            toggleGrafik = function(grafikName) {{
                grafiki[grafikName].hiddenState = !grafiki[grafikName].hiddenState 
                if (grafiki[grafikName].hiddenState) {{ 
                    view.hideColumns([grafiki[grafikName].id])
                }}
                else {{
                    var restore = view.getViewColumns()
                    console.log('getViewColumns', restore)
                    restore.push(grafiki[grafikName].id)
                    view.setColumns(restore.sort())
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
            console.log('SERIES START: ', options.colors);    
        }}
        </script>
    </head>
    <body>
        <div style="width: 100%;">
            
            <div id="chart_div" style="display: block; width: 1500px; height: 95%; padding-top: 0px; margin: -100px auto 0"; position: relative; z-index: -100>
            </div>
            <div id="APIErrorMessage" style="width: 900px; margin: auto; text-align: center; color: red">
            </div>
            <div id="dataUpdateErrorMessage" style="width: 900px; margin: auto; text-align: center; color: red">
            </div>
            <div style="width: 900px; margin: auto">
                <a onclick=toggleGrafik("Tkol") class="waves-effect waves-light btn-small">Tkol</a>
                <a onclick=toggleGrafik("Tniz") class="waves-effect waves-light btn-small">Tniz</a>
                <a onclick=toggleGrafik("Tyl") class="waves-effect waves-light btn-small">Tyl</a>
                <a onclick=toggleGrafik("dT") class="waves-effect waves-light btn-small">dT</a>
                <a onclick=toggleGrafik("STns") class="waves-effect waves-light btn-small">STns</a>
                <a onclick=toggleGrafik("STnag") class="waves-effect waves-light btn-small">STnag</a>
                <a onclick=toggleGrafik("Tkom") class="waves-effect waves-light btn-small">Tkom</a>
                <a onclick=toggleGrafik("Tkol2") class="waves-effect waves-light btn-small">Tkol2</a>
                <a class="waves-effect waves-light btn-small grey" id="nasos">Насос</a>
                <a class="waves-effect waves-light btn-small grey" id="nagrev">Нагрев</a>
            </div>
            <div style="width: 900px; margin: auto"; text-align: left;">
                <h6>History data: </h6>
                            
                {history_data}
                            
            </div>
        </div>
    </body>
    <script>
        var status_nasos_nagrev = {status_nasos_nagrev}
        var status_nasos = status_nasos_nagrev.status_relay.status_nasos 
        var status_nagrev = status_nasos_nagrev.status_relay.status_nagrev
        var nasos = document.getElementById("nasos");
        var nagrev = document.getElementById("nagrev");
        var APIErrorMessage = document.getElementById("APIErrorMessage");
        var dataUpdateErrorMessage = document.getElementById("dataUpdateErrorMessage");
        
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