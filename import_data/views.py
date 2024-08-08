import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from .models import Terminal
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import psycopg2
from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db.models import Sum, Count




# Define custom column headings
column_headings = {
    'state': 'State',
    'station_code': 'Terminal Code',
    'station_name': 'Terminal Name',
    'division': 'Division',
    'zone': 'Zone',
    'district': 'District',
    'terminal_type': 'Terminal Type',
    'working_hours_from': 'Working Hours From',
    'working_hours_to': 'Working Hours To',
    'avg_rakes_handling': 'Average Rakes Handling',
    'line_count': 'Line Count',
    'handling_type': 'Handling Type',
    'warehouse_available_yes_no': 'Warehouse Available',
    'owner': 'Owner',
    'associated_weighbridge': 'Associated Weighbridge',
    'alternate_weighbridge': 'Alternate Weighbridge',
    'tank_handling_yes_no': 'Tank Handling'
}
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def home(request):
    return render(request, 'import_data/home.html')

def display_data(request):
    try:
        total_data_points = Terminal.objects.count()
        states = Terminal.objects.values_list('state', flat=True).distinct()
        states = [state.title() for state in states if state]
        state_counts = Terminal.objects.values('state').annotate(count=Count('state')).order_by('state')
        state_counts = [(state['state'].title(), state['count']) for state in state_counts]

        selected_state = request.GET.get('state', '')

        if selected_state:
            filtered_df = pd.DataFrame(list(Terminal.objects.filter(state__iexact=selected_state.upper()).values()))
        else:
            filtered_df = pd.DataFrame(list(Terminal.objects.all().values()))

        filtered_df.rename(columns=column_headings, inplace=True)
        filtered_df = filtered_df.apply(lambda col: col.fillna("N/A") if col.dtype == 'O' else col)
        if 'Line Count' in filtered_df.columns:
            filtered_df['Line Count'] = filtered_df['Line Count'].fillna("N/A")
        if 'Terminal Name' in filtered_df.columns:
            filtered_df['Terminal Name'] = filtered_df['Terminal Name'].str.title()
        if 'District' in filtered_df.columns:
            filtered_df['District'] = filtered_df['District'].str.title()
        if 'State' in filtered_df.columns:
            filtered_df['State'] = filtered_df['State'].str.title()
        if 'latitude' in filtered_df.columns and 'longitude' in filtered_df.columns:
            filtered_df.drop(columns=['latitude', 'longitude'], inplace=True)
        if 'Working Hours From' in filtered_df.columns and 'Working Hours To' in filtered_df.columns:
            filtered_df['Working Hours From'] = filtered_df.apply(
                lambda row: "N/A" if row['Working Hours From'] == "N/A" and row['Working Hours To'] == "N/A" else f"{row['Working Hours From']} to {row['Working Hours To']}",
                axis=1
            )
            filtered_df.drop(columns=['Working Hours To'], inplace=True)
        if 'Warehouse Available' in filtered_df.columns:
            filtered_df['Warehouse Available'] = filtered_df['Warehouse Available'].replace({'Y': 'Yes', 'N': 'No'})
        if 'Tank Handling' in filtered_df.columns:
            filtered_df['Tank Handling'] = filtered_df['Tank Handling'].replace({'Y': 'Yes', 'N': 'No'})
        if 'id' in filtered_df.columns:
            filtered_df.drop(columns=['id'], inplace=True)
        if 'Warehouse Available' in filtered_df.columns:
            filtered_df.drop(columns=['Warehouse Available'], inplace=True)
        if 'Tank Handling' in filtered_df.columns:
            filtered_df.drop(columns=['Tank Handling'], inplace=True)
        if 'Alternate Weighbridge' in filtered_df.columns:
            filtered_df.drop(columns=['Alternate Weighbridge'], inplace=True)
        if 'Associated Weighbridge' in filtered_df.columns:
            filtered_df.drop(columns=['Associated Weighbridge'], inplace=True)
            

        if not selected_state:
            table_html = None
        else:
            table_html = filtered_df.to_html(classes="table table-striped table-bordered", index=False)

        return render(request, 'import_data/display_data.html', {
            'states': states,
            'selected_state': selected_state,
            'state_counts': state_counts,
            'table_html': table_html,
            'total_data_points': total_data_points
        })
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, 'import_data/display_data.html', {
            'states': [],
            'selected_state': '',
            'state_counts': [],
            'table_html': None,
            'total_data_points': 0,
            'error': str(e)
        })

def map_view(request):
    try:
        states = Terminal.objects.values_list('state', flat=True).distinct()
        states = [state.title() for state in states if state]
        
        terminals = Terminal.objects.all()
        df = pd.DataFrame(list(terminals.values()))
        df.rename(columns=column_headings, inplace=True)
        
        terminal_type_counts = df['Terminal Type'].value_counts().reset_index()
        terminal_type_counts.columns = ['terminal_type', 'count']
        chart_data = terminal_type_counts.to_dict(orient='records')
        
        return render(request, 'import_data/map.html', {'states': states, 'chart_data': chart_data})
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, 'import_data/map.html', {'states': [], 'chart_data': [], 'error': str(e)})


def get_geojson(request):
    state = request.GET.get('state', None)

    if state:
        terminals = Terminal.objects.filter(state__iexact=state.upper())
    else:
        terminals = Terminal.objects.all()

    features = []
    for terminal in terminals:
        features.append({
            "type": "Feature",
            "properties": {
                "id": terminal.id,
                "terminal_code": terminal.station_code,
                "division": terminal.division,
                "zone": terminal.zone,
                "district": terminal.district.title() if terminal.district else "N/A",
                "state": terminal.state.title() if terminal.state else "N/A",
            },
            "geometry": {
                "type": "Point",
                "coordinates": [terminal.longitude, terminal.latitude]
            }
        })
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    try:
        connection = psycopg2.connect(
            dbname='terminals',
            user='kt',
            password='ktsdb1',
            host='localhost',
            port='5432'
        )
        cursor = connection.cursor()

        if state:
            cursor.execute("SELECT station_code FROM terminal_data WHERE state = %s", (state,))
            station_codes = cursor.fetchall()
            station_codes = [code[0] for code in station_codes]
        else:
            cursor.execute("SELECT station_code FROM terminal_data")
            station_codes = cursor.fetchall()
            station_codes = [code[0] for code in station_codes]

        if station_codes:
            format_strings = ','.join(['%s'] * len(station_codes))
            query = f"""
            SELECT EXTRACT(MONTH FROM month) AS month, EXTRACT(YEAR FROM month) AS year, 
                   SUM(earning_in_rs_cr), SUM(loading_in_mt), SUM(unloading_in_mt)
            FROM ldn_unldn_revenue
            WHERE station_code IN ({format_strings}) AND (EXTRACT(YEAR FROM month) = 2023 OR EXTRACT(YEAR FROM month) = 2024)
            GROUP BY EXTRACT(MONTH FROM month), EXTRACT(YEAR FROM month)
            ORDER BY year, month;
            """
            cursor.execute(query, station_codes)
            rows = cursor.fetchall()

            earnings_data = [['Month', '2023 Earnings', '2024 Earnings']]
            loading_data = [['Month', '2023 Loading', '2024 Loading']]
            unloading_data = [['Month', '2023 Unloading', '2024 Unloading']]
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            earnings_2023 = [0] * 12
            earnings_2024 = [0] * 12
            loading_2023 = [0] * 12
            loading_2024 = [0] * 12
            unloading_2023 = [0] * 12
            unloading_2024 = [0] * 12

            for row in rows:
                month = int(row[0]) - 1
                year = int(row[1])
                earning = float(row[2])
                loading = float(row[3])
                unloading = float(row[4])

                if year == 2023:
                    earnings_2023[month] = earning
                    loading_2023[month] = loading
                    unloading_2023[month] = unloading
                elif year == 2024:
                    earnings_2024[month] = earning
                    loading_2024[month] = loading
                    unloading_2024[month] = unloading

            for i in range(12):
                earnings_data.append([months[i], earnings_2023[i], earnings_2024[i]])
                loading_data.append([months[i], loading_2023[i], loading_2024[i]])
                unloading_data.append([months[i], unloading_2023[i], unloading_2024[i]])

            if state:
                total_earnings = sum(earnings_2024)
                total_loading = sum(loading_2024)
                total_unloading = sum(unloading_2024)
                total_terminals = terminals.count()

                state_data = {
                    "total_earnings": total_earnings,
                    "total_loading": total_loading,
                    "total_unloading": total_unloading,
                    "total_terminals": total_terminals,
                    "earnings_data": earnings_data,
                    "loading_data": loading_data,
                    "unloading_data": unloading_data
                }

                # Calculate the terminal type distribution for the state
                terminal_type_counts = Terminal.objects.filter(state__iexact=state.upper()).values('terminal_type').annotate(count=Count('terminal_type'))
                pie_chart_data = [['Terminal Type', 'Count']]
                for entry in terminal_type_counts:
                    pie_chart_data.append([entry['terminal_type'], entry['count']])
                
                state_data["pie_chart_data"] = pie_chart_data

                geojson["state_data"] = state_data
            else:
                total_earnings = sum(earnings_2024)
                total_loading = sum(loading_2024)
                total_unloading = sum(unloading_2024)
                total_terminals = terminals.count()

                india_data = {
                    "total_earnings": total_earnings,
                    "total_loading": total_loading,
                    "total_unloading": total_unloading,
                    "total_terminals": total_terminals,
                    "earnings_data": earnings_data,
                    "loading_data": loading_data,
                    "unloading_data": unloading_data
                }

                # Calculate the terminal type distribution for entire India
                terminal_type_counts_india = Terminal.objects.values('terminal_type').annotate(count=Count('terminal_type'))
                pie_chart_data_india = [['Terminal Type', 'Count']]
                for entry in terminal_type_counts_india:
                    pie_chart_data_india.append([entry['terminal_type'], entry['count']])
                
                india_data["pie_chart_data"] = pie_chart_data_india

                geojson["india_data"] = india_data

    except Exception as e:
        print(f"An error occurred: {e}")

    return JsonResponse(geojson)




def get_terminal_details(request, terminal_id):
    try:
        terminal = Terminal.objects.get(id=terminal_id)
        terminal_data = {
            "station_name": terminal.station_name or "N/A",
            "working_hours_from": terminal.working_hours_from or "N/A",
            "working_hours_to": terminal.working_hours_to or "N/A",
            "terminal_type": terminal.terminal_type or "N/A",
            "avg_rakes_handling": terminal.avg_rakes_handling or "N/A",
            "line_count": terminal.line_count or "N/A",
            "handling_type": terminal.handling_type or "N/A",
            "warehouse_available_yes_no": terminal.warehouse_available_yes_no.replace("Y", "Yes").replace("N", "No") if terminal.warehouse_available_yes_no else "N/A",
            "owner": terminal.owner or "N/A",
            "associated_weighbridge": terminal.associated_weighbridge or "N/A",
            "alternate_weighbridge": terminal.alternate_weighbridge or "N/A",
            "tank_handling_yes_no": terminal.tank_handling_yes_no.replace("Y", "Yes").replace("N", "No") if terminal.tank_handling_yes_no else "N/A"
        }

        # Fetch earnings, loading, and unloading data from the second table
        connection = psycopg2.connect(
            dbname='terminals',
            user='kt',
            password='ktsdb1',
            host='localhost',
            port='5432'
        )
        cursor = connection.cursor()
        query = """
        SELECT EXTRACT(MONTH FROM month) AS month, EXTRACT(YEAR FROM month) AS year, 
               SUM(earning_in_rs_cr), SUM(loading_in_mt), SUM(unloading_in_mt)
        FROM ldn_unldn_revenue
        WHERE station_code = %s AND (EXTRACT(YEAR FROM month) = 2023 OR EXTRACT(YEAR FROM month) = 2024)
        GROUP BY EXTRACT(MONTH FROM month), EXTRACT(YEAR FROM month)
        ORDER BY year, month;
        """
        cursor.execute(query, (terminal.station_code,))
        rows = cursor.fetchall()

        # Process the results into the format needed for Google Charts
        earnings_data = [['Month', '2023 Earnings', '2024 Earnings']]
        loading_data = [['Month', '2023 Loading', '2024 Loading']]
        unloading_data = [['Month', '2023 Unloading', '2024 Unloading']]
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        earnings_2023 = [0] * 12
        earnings_2024 = [0] * 12
        loading_2023 = [0] * 12
        loading_2024 = [0] * 12
        unloading_2023 = [0] * 12
        unloading_2024 = [0] * 12

        for row in rows:
            month = int(row[0]) - 1  # 0-based index for months
            year = int(row[1])
            earning = float(row[2])
            loading = float(row[3])
            unloading = float(row[4])

            if year == 2023:
                earnings_2023[month] = earning
                loading_2023[month] = loading
                unloading_2023[month] = unloading
            elif year == 2024:
                earnings_2024[month] = earning
                loading_2024[month] = loading
                unloading_2024[month] = unloading

        for i in range(12):
            earnings_data.append([months[i], earnings_2023[i], earnings_2024[i]])
            loading_data.append([months[i], loading_2023[i], loading_2024[i]])
            unloading_data.append([months[i], unloading_2023[i], unloading_2024[i]])

        terminal_data["earnings_data"] = earnings_data
        terminal_data["loading_data"] = loading_data
        terminal_data["unloading_data"] = unloading_data

        return JsonResponse(terminal_data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
