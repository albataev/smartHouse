html_data = '''
<html>
    <head>
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
        
        var on2 = document.getElementById("on2");
        var off2 = document.getElementById("off2");
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

        on1.onclick = function() {{
            var xhr1 = new XMLHttpRequest();
            xhr1.open('GET', "http://192.168.1.50/on1", true);
            xhr1.send();
            xhr1.onreadystatechange = function() {{ // (3)
                if (xhr1.readyState != 4) return;
                if (xhr1.status != 200) {{
                    alert(xhr1.status + ': ' + xhr1.statusText);
                }} else {{
                    alert(xhr1.responseText);
                }}
            }}
        }}
        
        off1.onclick = function() {{
            var xhr = new XMLHttpRequest();
            xhr.open('GET', "http://192.168.1.50/off1", true);
            xhr.send();
                xhr.onreadystatechange = function() {{ // (3)
                if (xhr.readyState != 4) return;
                if (xhr.status != 200) {{
                    alert(xhr.status + ': ' + xhr.statusText);
                }} else {{
                    alert(xhr.responseText);
                }}
            }}
        }}

        on2.onclick = function() {{
            var xhr1 = new XMLHttpRequest();
            xhr1.open('GET', "http://192.168.1.50/on2", true);
            xhr1.send();
            xhr1.onreadystatechange = function() {{ // (3)
                if (xhr1.readyState != 4) return;
                if (xhr1.status != 200) {{
                    alert(xhr1.status + ': ' + xhr1.statusText);
                }} else {{
                    alert(xhr1.responseText);
                }}
            }}
        }}
        
        off2.onclick = function() {{
            var xhr = new XMLHttpRequest();
            xhr.open('GET', "http://192.168.1.50/off2", true);
            xhr.send();
                xhr.onreadystatechange = function() {{ // (3)
                    if (xhr.readyState != 4) return;
                    if (xhr.status != 200) {{
                        alert(xhr.status + ': ' + xhr.statusText);
                    }} else {{
                        alert(xhr.responseText);
                    }}
                }}
            }}
        }}
        </script>
    </head>
    <body>
        <div style="width: 100%;">
            <div id="chart_div" style="display: block; width: 1500px; height: 95%; padding-top: 0px; margin: -100px auto 0"; position: relative; z-index: -100>
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
                <a class="waves-effect waves-light btn-small" id="on1">on1</a>
                <a class="waves-effect waves-light btn-small" id="off1">off1</a>
                <a class="waves-effect waves-light btn-small" id="on2">/on2</a>
                <a class="waves-effect waves-light btn-small" id="off2">/off2</a>
            </div>
            <div style="width: 900px; margin: auto"; text-align: left;">
                <h6>History data: </h6>
                            
                {history_data}
                            
            </div>
        </div>
    </body>
</html>'''