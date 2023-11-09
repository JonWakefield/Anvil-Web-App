### File outlines the contents of each directory, showcasing where each file can be found.

#### Pides_VIEWER File Structure:

    Pides_VIEWER/
    |
    |___ README.md
    |___ LICENSE.txt
    |___ requirements.txt
    |___ __init__.py
    |___ .anvil_editor.yaml
    |___ .gitignore
    |___ anvil.yaml
    |
    |___ logs/
    |        |
    |        |___error_log.txt
    |        |___debug_log.txt
    | 
    |
    |——— server_code/
    |        |
    |        |——— anvil_uplink_router.py
    |        |——— add_users.py
    |        |___ Globals.py
    |        |
    |        |——— uplink_scripts/
    |        |       |
    |        |       |——— camera_controls_uplink.py
    |        |       |——— gin_monitor_uplink.py
    |        |       |——— nodeS_connected_uplink.py
    |        |       |——— picture_capture_controls_uplink.py
    |        |       |——— stack.py
    |        |       |——— user_management.py
    |        |       |——— graphs_uplink.py
    |        |       |——— graphs/
    |        |               |
    |        |               |___ bar_chart.py
    |        |               |___ pie_chart.py
    |        |               |——— scatter_chart.py
    |        |               |——— timeline_chart.py   
    |        |
    |        |——— utils/
    |                |
    |                |___ create_db_tables.py
    |                |___ dateTime_utils.py
    |                |___ json_utils.py
    |                |___ log_errors_utils.py
    |                |___ mySQL_utils.py
    |                |___ Pandas_utils.py
    |                |___ simulate_imageAges.py
    |                |___ simulate_plastic_events.py
    |
    |
    |___ client_code/
    |        |
    |        |___ MainModule.py
    |        |___ Globals.py
    |        |
    |        |___ FormCamControls/
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormEnlargedImage/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormGinMonitoring/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormGraphSetup/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormHomePage/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormLandingPage/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormNodeConns/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormPicCapControls/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormRoutingError/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormSettings/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ FormTrendGraphs/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ MainRouter/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ RequestAccessModal/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |        |       
    |        |___ SignInModal/       
    |        |       |___ __init__.py
    |        |       |___ form_template.yaml
    |
    |
    |___ theme/
    |        |
    |        |___ parameters.yaml
    |        |___ templates.yaml
    |        |
    |        |___ assets/
    |                |
    |                |___ dashboard.html
    |                |___ single-column.html

    
    
            
