from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import pandas as pd
from django.contrib.auth.decorators import login_required  # for login authentication for veiwing next pages after login
from .forms import CreateUserForm
from django.contrib import messages
import json
from django.core.files.storage import default_storage
import os
import numpy as np



# request page
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'accounts/register.html', context)


##login page
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('fileupload')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            # chek user exist
            if user is not None:
                login(request, user)
                return redirect('fileupload')
            else:
                messages.info(request, 'User Name or Password is incorrect')
        context = {}
        return render(request, 'accounts/login.html', context)


# logoutpage
def logoutUser(request):
    path = 'uploads/' + str(request.session.get('uploadedFileName'))
    if os.path.isfile(path):
        os.remove(path)
    logout(request)
    request.session.clear()
    return redirect('login')


### Utilization Graphs Page / Utilization HTML page
@login_required(login_url='login')
def home(request):
    ##line chart for Fuel
    dateRange1 = None
    dateRange2 = None

    # linechart1
    temp1 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.CONTAINERS.HANDLED.40FT'].reset_index(inplace=False)
    temp2 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.CONTAINERS.HANDLED.40FT'].reset_index(inplace=False)

    temp11 = pd.merge(temp1, temp2, on=['tag_name', 'id_date', 'hours'])
    final_df = temp11[['unique_x', 'value_x', 'value_y']]
    final_df['index'] = final_df.index
    final_df.columns = ['unique', 'M1055', 'M311', 'index']
    final_df = final_df[['index', 'M1055', 'M311']]
    final_df = [final_df.columns.values.tolist()] + final_df.values.tolist()
    linechart_util = json.dumps(final_df)

    ##line chart 2
    temp3 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.LOAD'].reset_index(inplace=False)
    temp4 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.LOAD'].reset_index(inplace=False)

    temp22 = pd.merge(temp3, temp4, on=['tag_name', 'id_date', 'hours'])
    final_df1 = temp22[['unique_x', 'value_x', 'value_y']]
    final_df1['index'] = final_df1.index
    final_df1.columns = ['unique', 'M1055', 'M311', 'index']
    final_df1 = final_df1[['index', 'M1055', 'M311']]
    final_df1 = [final_df1.columns.values.tolist()] + final_df1.values.tolist()
    linechart_util1 = json.dumps(final_df1)

    # line chart 3
    temp5 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.LOAD.WEIGHT'].reset_index(inplace=False)
    temp6 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.LOAD.WEIGHT'].reset_index(inplace=False)

    temp33 = pd.merge(temp5, temp6, on=['tag_name', 'id_date', 'hours'])
    final_df2 = temp33[['unique_x', 'value_x', 'value_y']]
    final_df2['index'] = final_df2.index
    final_df2.columns = ['unique', 'M1055', 'M311', 'index']
    final_df2 = final_df2[['index', 'M1055', 'M311']]
    final_df2 = [final_df2.columns.values.tolist()] + final_df2.values.tolist()
    linechart_util2 = json.dumps(final_df2)

    return render(request, 'accounts/dashboard.html',
                  {'linechart_util': linechart_util, 'linechart_util1': linechart_util1,
                   'linechart_util2': linechart_util2})


@login_required(login_url='login')
def products(request):
    return render(request, 'accounts/products.html')


@login_required(login_url='login')
def about(request):
    return render(request, 'accounts/about.html')


@login_required(login_url='login')
def customer(request):
    return render(request, 'accounts/customer.html')


@login_required(login_url='login')
##overview html page
def overview(request):
    ## reading the xlsx fles
    if request.method == 'GET':
        return render(request, 'accounts/overview.html')

    if request.method == 'POST':
        kpi = request.POST.get('kpis', None)
        subkpis = request.POST.get('subkpis', None)
        prices = {"Performance": ["Trips", "Tonnage", "Delay"],
                  "Operational": ["Trains", "Average Load Time", "Average Tonnage", "Total wagons"],
                  "Product": ['Glycol specific reports', 'Average Robo Time'],
                  }
        subkpis = prices[kpi][int(subkpis) - 1]
        if (kpi == "Performance") & (subkpis == "Trips"):
            name = '../../static/graphs/NumberOfDepartresPerDay.png'
            name1 = '../../static/graphs/NumberOfDepartresPerHour.png'
            return render(request, 'accounts/overview.html', {"name": name, "name1": name1})
        elif (kpi == "Performance") & (subkpis == "Tonnage"):
            name = '../../static/graphs/TrainTonnage.png'
            return render(request, 'accounts/overview.html', {"name2": name})
        elif (kpi == "Operational") & (subkpis == "Average Tonnage"):
            name = '../../static/graphs/Tonnes per day.png'
            return render(request, 'accounts/overview.html', {"name2": name})
        elif (kpi == "Operational") & (subkpis == "Average Load Time"):
            name = '../../static/graphs/Trains by tonnes and Load Time.png'
            return render(request, 'accounts/overview.html', {"name": name})
        elif (kpi == "Operational") & (subkpis == "Total wagons"):
            name = '../../static/graphs/Trains by tonnes and Wagons Tonnes.png'
            name1 = '../../static/graphs/Trains by tonnes and Wagons.png'
            name2 = '../../static/graphs/NumberofWagons.png'
            return render(request, 'accounts/overview.html', {"name": name, 'name1': name1, 'name2': name2})
        elif (kpi == "Product") & (subkpis == "Glycol specific reports"):
            name = '../../static/graphs/glycol.png'
            name1 = '../../static/graphs/Stacked Glycol.png'
            return render(request, 'accounts/overview.html', {"glycol": name, 'glycol1': name1})
        elif (kpi == "Product") & (subkpis == "Average Robo Time"):
            name = '../../static/graphs/Average Robot Time.png'
            name1 = '../../static/graphs/Average Robot Time-time.png'
            return render(request, 'accounts/overview.html', {"avgrd": name, 'avgrt': name1})
        #  return render(request, 'accounts/overview.html',
        #                {'barchart_util': barchart_util, "barchart_util1": barchart_util1, 'value': value,
        #                 'units': units})
        else:
            return render(request, 'accounts/metricselection.html',
                          {'Message': 'Unable to display the Graph .The selected tag has less Data',
                           'value': "tagname"})


@login_required(login_url='login')
def trains(request):
    if request.method == 'GET':
        return render(request, 'accounts/trains.html')

    if request.method == 'POST':
        train = request.POST.get('train_no', None)

        if train == "None":
            return render(request, 'accounts/trains.html', {'context': 'Please select and option'})
        #graph(train)
        wagons = '../../static/train_graphs/'+train+'_WAGONS.png'
        RT = '../../static/train_graphs/'+train+'_RT.png'
        tons = '../../static/train_graphs/'+train+'_TONS.png'
        LT = '../../static/train_graphs/'+train+'_LT.png'
        ST = '../../static/train_graphs/'+train+'_ST.png'
        tons_minute = '../../static/train_graphs/'+train+'_tons_minute.png'
        tons_wagon = '../../static/train_graphs/'+train+'_tons_wagon.png'

        return render(request, 'accounts/trains.html',
                      {'wagons': wagons, 'RT': RT, 'tons': tons, 'tons_wagon': tons_wagon,
                       'tons_minute': tons_minute, 'LT': LT, "ST": ST})


##reading the xlsx file and validating it
@login_required(login_url='login')
def fileupload(request):
    if request.method == 'GET':
        return render(request, 'accounts/input.html', {})
    elif request.FILES["excel_file"].name.split('.')[-1] not in ['xls', 'xlsx']:
        return render(request, 'accounts/input.html', {'error': 'upload only xlsx/xls file format'})
    else:
        excel_file = request.FILES["excel_file"]
        # adding file name to the session
        request.session['uploadedFileName'] = excel_file.name
        # path = default_storage.save('uploads/temp.csv', ContentFile(excel_file.read()))
        # print("path---",path)
        with default_storage.open('uploads/' + excel_file.name, 'wb+') as destination:
            for chunk in excel_file.chunks():
                destination.write(chunk)
        # file_name = default_storage.save('temp.csv', excel_file)
        # file_url = default_storage.url(file_name)
        column_data = pd.read_excel('uploads/' + excel_file.name)
        # filteredColumns = list(column_data.dtypes[column_data.dtypes != np.object].index)
        filteredColumns = list(column_data.dtypes[column_data.dtypes != np.object].index)
        request.session['filterColumns'] = filteredColumns

        return render(request, 'accounts/input.html', {'column_data': column_data.to_html(index=False)})


# for metric selection / Metric selection HTML Page
def metricSelection(request):
    ##line chart for Fuel
    dateRange1 = pd.read_csv("Mega Industries/telemetry_machine1_Movement.csv")
    dateRange2 = pd.read_csv("Mega Industries/telemetry_machine2_Movement.csv")

    # linechart1
    temp1 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.ENGINE.SPEED'].reset_index(inplace=False)
    temp2 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.ENGINE.SPEED'].reset_index(inplace=False)

    temp11 = pd.merge(temp1, temp2, on=['tag_name', 'id_date', 'hours'])
    final_df = temp11[['unique_x', 'value_x', 'value_y']]
    final_df['index'] = final_df.index
    final_df.columns = ['unique', 'M1055', 'M311', 'index']
    final_df = final_df[['index', 'M1055', 'M311']]
    final_df = [final_df.columns.values.tolist()] + final_df.values.tolist()
    linechart_util = json.dumps(final_df)

    ##line chart 2
    temp3 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.VISCO.FAN.SPEED'].reset_index(inplace=False)
    temp4 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.VISCO.FAN.SPEED'].reset_index(inplace=False)

    temp22 = pd.merge(temp3, temp4, on=['tag_name', 'id_date', 'hours'])
    final_df1 = temp22[['unique_x', 'value_x', 'value_y']]
    final_df1['index'] = final_df1.index
    final_df1.columns = ['unique', 'M1055', 'M311', 'index']
    final_df1 = final_df1[['index', 'M1055', 'M311']]
    final_df1 = [final_df1.columns.values.tolist()] + final_df1.values.tolist()
    linechart_util1 = json.dumps(final_df1)

    # line chart 3
    temp5 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.TOTAL.DRIVING.DISTANCE.DECIMAL'].reset_index(inplace=False)
    temp6 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.TOTAL.DRIVING.DISTANCE.DECIMAL'].reset_index(inplace=False)

    temp33 = pd.merge(temp5, temp6, on=['tag_name', 'id_date', 'hours'])
    final_df2 = temp33[['unique_x', 'value_x', 'value_y']]
    final_df2['index'] = final_df2.index
    final_df2.columns = ['unique', 'M1055', 'M311', 'index']
    final_df2 = final_df2[['index', 'M1055', 'M311']]
    final_df2 = [final_df2.columns.values.tolist()] + final_df2.values.tolist()
    linechart_util2 = json.dumps(final_df2)

    return render(request, 'accounts/metricselection.html',
                  {'linechart_util': linechart_util, 'linechart_util1': linechart_util1,
                   'linechart_util2': linechart_util2})


# for graph display for tab /  Fuel Consumption Html page
@login_required(login_url='login')
def graphdisplay(request):
    ##Graph2
    ## reading the csv file for fuel
    # M1 machine data
    telemetry_machine1_fuel = pd.read_csv("C:/Mega Industries/telemetry_machine1_fuel.csv")
    res1 = telemetry_machine1_fuel.groupby('tag_name').agg({'value': ['mean', 'min', 'max', 'count']})
    res1.columns = ['mean', 'min', 'max', 'count']
    res1['tag_name'] = res1.index

    # machine M2
    telemetry_machine1_fuel2 = pd.read_csv("C:/Mega Industries/telemetry_machine2_fuel.csv")
    res2 = telemetry_machine1_fuel2.groupby('tag_name').agg({'value': ['mean', 'min', 'max', 'count']})
    res2.columns = ['mean', 'min', 'max', 'count']
    res2['tag_name'] = res2.index

    # pie chart M1
    pie1 = res1[['tag_name', 'count']]
    pie1 = [pie1.columns.values.tolist()] + pie1.values.tolist()
    pie_m1 = json.dumps(pie1)

    # pie chart M2
    pie2 = res2[['tag_name', 'count']]
    pie2 = [pie2.columns.values.tolist()] + pie2.values.tolist()
    pie_m2 = json.dumps(pie2)

    ##bar chart M1
    bar_res = telemetry_machine1_fuel.groupby(['tag_name', 'id_date']).agg({'value': ['mean', 'min', 'max', 'count']})
    bar_res.columns = ['mean', 'min', 'max', 'count']
    bar_res['tag_name_id'] = bar_res.index
    bar_res['mean'] = bar_res['mean'].astype(int)
    # seperating tha values by _
    bar_res['id_date'] = bar_res['tag_name_id'].str.get(1)
    bar_res['tag_name'] = bar_res['tag_name_id'].str.get(0)
    bar_res['tag_name_id'] = bar_res['id_date'].str.cat(bar_res['tag_name'], sep="_")
    bar_res1 = bar_res[['tag_name_id', 'mean', 'min', 'max']]

    bar1 = [bar_res1.columns.values.tolist()] + bar_res1.values.tolist()
    bar1_m1 = json.dumps(bar1)

    # bar chart m2
    bar_res2 = telemetry_machine1_fuel2.groupby(['tag_name', 'id_date']).agg({'value': ['mean', 'min', 'max', 'count']})
    bar_res2.columns = ['mean', 'min', 'max', 'count']
    bar_res2['tag_name_id'] = bar_res2.index
    bar_res2['mean'] = bar_res2['mean'].astype(int)
    # seperating tha values by _
    bar_res2['id_date'] = bar_res2['tag_name_id'].str.get(1)
    bar_res2['tag_name'] = bar_res2['tag_name_id'].str.get(0)
    bar_res2['tag_name_id'] = bar_res2['id_date'].str.cat(bar_res['tag_name'], sep="_")
    bar_res22 = bar_res2[['tag_name_id', 'mean', 'min', 'max']]

    bar2 = [bar_res22.columns.values.tolist()] + bar_res22.values.tolist()
    bar2_m2 = json.dumps(bar2)

    ##Line Charts
    clm1 = bar_res[['tag_name_id', 'count']]
    clm2 = bar_res2[['tag_name_id', 'count']]

    fuel_df = pd.merge(clm1, clm2, on="tag_name_id")
    fuel_df = [fuel_df.columns.values.tolist()] + fuel_df.values.tolist()
    linechart_m1m2 = json.dumps(fuel_df)

    ##line chart for Fuel
    dateRange1 = pd.read_csv("Mega Industries/telemetry_machine1_fuel_daterange.csv")
    dateRange2 = pd.read_csv("Mega Industries/telemetry_machine2_fuel_daterange.csv")

    # linechart1
    temp1 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.FUEL.RATE'].reset_index(inplace=False)
    temp2 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.FUEL.RATE'].reset_index(inplace=False)

    temp11 = pd.merge(temp1, temp2, on=['tag_name', 'id_date', 'hours'])
    final_df = temp11[['unique_x', 'value_x', 'value_y']]
    final_df['index'] = final_df.index
    final_df.columns = ['unique', 'M1055', 'M311', 'index']
    final_df = final_df[['index', 'M1055', 'M311']]
    final_df = [final_df.columns.values.tolist()] + final_df.values.tolist()
    linechart_fuel = json.dumps(final_df)

    ##line chart 2
    temp3 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.TRIP.FUEL.CONSUMPTION'].reset_index(inplace=False)
    temp4 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.TRIP.FUEL.CONSUMPTION'].reset_index(inplace=False)

    temp22 = pd.merge(temp3, temp4, on=['tag_name', 'id_date', 'hours'])
    final_df1 = temp22[['unique_x', 'value_x', 'value_y']]
    final_df1['index'] = final_df1.index
    final_df1.columns = ['unique', 'M1055', 'M311', 'index']
    final_df1 = final_df1[['index', 'M1055', 'M311']]
    final_df1 = [final_df1.columns.values.tolist()] + final_df1.values.tolist()
    linechart_fuel1 = json.dumps(final_df1)

    # line chart 3
    temp5 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.HYDRAULIC.TANK.LEVEL'].reset_index(inplace=False)
    temp6 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.HYDRAULIC.TANK.LEVEL'].reset_index(inplace=False)

    temp33 = pd.merge(temp5, temp6, on=['tag_name', 'id_date', 'hours'])
    final_df2 = temp33[['unique_x', 'value_x', 'value_y']]
    final_df2['index'] = final_df2.index
    final_df2.columns = ['unique', 'M1055', 'M311', 'index']
    final_df2 = final_df2[['index', 'M1055', 'M311']]
    final_df2 = [final_df2.columns.values.tolist()] + final_df2.values.tolist()
    linechart_fuel2 = json.dumps(final_df2)

    return render(request, 'accounts/graphs.html',
                  {'pie_m1': pie_m1, 'pie_m2': pie_m2, 'bar1_m1': bar1_m1, 'bar2_m2': bar2_m2,
                   'linechart_m1m2': linechart_m1m2, 'linechart_fuel': linechart_fuel,
                   'linechart_fuel1': linechart_fuel1, 'linechart_fuel2': linechart_fuel2})


# outputPage / Vitals Monitoring HTML Page
@login_required(login_url='login')
def outputPage(request):
    ##line chart for Fuel
    dateRange1 = pd.read_csv("Mega Industries/telemetry_machine1_vitals.csv")
    dateRange2 = pd.read_csv("Mega Industries/telemetry_machine2_vitals.csv")

    # linechart1
    temp1 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.HYDRAULIC.OIL.TEMPERATURE'].reset_index(inplace=False)
    temp2 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.HYDRAULIC.OIL.TEMPERATURE'].reset_index(inplace=False)

    temp11 = pd.merge(temp1, temp2, on=['tag_name', 'id_date', 'hours'])
    final_df = temp11[['unique_x', 'value_x', 'value_y']]
    final_df['index'] = final_df.index
    final_df.columns = ['unique', 'M1055', 'M311', 'index']
    final_df = final_df[['index', 'M1055', 'M311']]
    final_df = [final_df.columns.values.tolist()] + final_df.values.tolist()
    linechart_util = json.dumps(final_df)

    ##line chart 2
    temp3 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.OIL.PRESSURE'].reset_index(inplace=False)
    temp4 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.OIL.PRESSURE'].reset_index(inplace=False)

    temp22 = pd.merge(temp3, temp4, on=['tag_name', 'id_date', 'hours'])
    final_df1 = temp22[['unique_x', 'value_x', 'value_y']]
    final_df1['index'] = final_df1.index
    final_df1.columns = ['unique', 'M1055', 'M311', 'index']
    final_df1 = final_df1[['index', 'M1055', 'M311']]
    final_df1 = [final_df1.columns.values.tolist()] + final_df1.values.tolist()
    linechart_util1 = json.dumps(final_df1)

    # line chart 3
    temp5 = dateRange1[dateRange1['tag_name'] == 'HT.PLC.INTAKE.TEMPERATURE'].reset_index(inplace=False)
    temp6 = dateRange2[dateRange2['tag_name'] == 'HT.PLC.INTAKE.TEMPERATURE'].reset_index(inplace=False)

    temp33 = pd.merge(temp5, temp6, on=['tag_name', 'id_date', 'hours'])
    final_df2 = temp33[['unique_x', 'value_x', 'value_y']]
    final_df2['index'] = final_df2.index
    final_df2.columns = ['unique', 'M1055', 'M311', 'index']
    final_df2 = final_df2[['index', 'M1055', 'M311']]
    final_df2 = [final_df2.columns.values.tolist()] + final_df2.values.tolist()
    linechart_util2 = json.dumps(final_df2)

    return render(request, 'accounts/output.html',
                  {'linechart_util': linechart_util, 'linechart_util1': linechart_util1,
                   'linechart_util2': linechart_util2})


@login_required(login_url='login')
def optimization(request):
    return render(request, 'accounts/optimization.html')


@login_required(login_url='login')
def gpstracking(request):
    if request.method == 'GET':
        df3 = pd.read_csv("Mega Industries/phase_2/M1&M2_datetime_cumReport.csv")
        df3 = df3[['value_lat', 'value_long', 'date_count', 'marker']]
        temp1 = df3[df3['marker'] == 'red'].head(200)
        temp2 = df3[df3['marker'] == 'blue'].head(200)
        final_df3 = pd.concat([temp1, temp2])
        final_df3 = [final_df3.columns.values.tolist()] + final_df3.values.tolist()
        googlechart3 = json.dumps(final_df3)
        return render(request, 'accounts/gpstracking.html', {'googlechart3': googlechart3})
    else:
        date_req = request.POST.get('date', None)
        # Machine wise cumulative movement
        df1 = pd.read_csv("Mega Industries/phase_2/M1&M2Cumulative.csv")
        print(df1.head())
        final_df2 = [df1.columns.values.tolist()] + df1.values.tolist()
        googlechart = json.dumps(final_df2)

        df3 = pd.read_csv("Mega Industries/phase_2/M1&M2_datetime_cumReport.csv")
        df4 = pd.read_csv("Mega Industries/phase_2/M1&M2dateCumulative.csv")

        print("The selected Date:", date_req)
        df3 = df3[df3['id_date'] == date_req]
        df3 = df3[['value_lat', 'value_long', 'date_count', 'marker']]
        temp1 = df3[df3['marker'] == 'red'].head(200)
        temp2 = df3[df3['marker'] == 'blue'].head(200)
        final_df3 = pd.concat([temp1, temp2])
        final_df3 = [final_df3.columns.values.tolist()] + final_df3.values.tolist()
        googlechart3 = json.dumps(final_df3)

        df4 = df4[df4['id_date'] == date_req]
        df4 = df4[['value_lat', 'value_long', 'date_count', 'marker']]
        temp3 = df4[df4['marker'] == 'red'].head(200)
        temp4 = df4[df4['marker'] == 'blue'].head(200)
        final_df4 = pd.concat([temp3, temp4])
        final_df4 = [final_df4.columns.values.tolist()] + final_df4.values.tolist()
        googlechart4 = json.dumps(final_df4)

        return render(request, 'accounts/gpstracking.html',
                      {'googlechart': googlechart, 'googlechart3': googlechart3, 'googlechart4': googlechart4})
