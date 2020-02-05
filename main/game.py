from matplotlib import pyplot as plt
import seaborn as sns
from colorama import Fore, Back, Style
from tabulate import tabulate
import csv
import sys
import random
from ship import Ship
from my_modules import *
from constants  import *

if len(sys.argv) >= 2:
    withRule = True if sys.argv[1] == 'rule' else False
else:
    withRule = False

def adapt_rule(oil_price,freight,exchange,own_ship,freight_data,time):
    average_freight = 0
    for data_index in range(10):
        if time - data_index < 0:
            average_freight += FREIGHT_PREV[time - data_index]
        else:
            average_freight += freight_data[time - data_index]['price']
    average_freight /= 10
    compare_list = [oil_price,freight,exchange,own_ship,average_freight]
    result = ''
    condition = ([[30,	140,	243.1619609,	2061.234867,	0,	243.4988243,	80,	140,	-1,	2212.740943],
                [0,	140,	-1,	2212.740943,	54.34868878,	180.4487791,	90,	120,	-1,	1455.210565],
                [-1,	-1,	-1,	-1,	0,	264.5155061,	30,	100,	1152.198414,	2364.247018]])
    '''
    condition = ([[30,	140,	701.8867087,	1764.517595,	0,	180.4244276,	-1,	-1,	550.0822963,	1764.517595],
                    [0,	140,    550.0822963,	1916.322007,	33.52070882,	243.3831642,	90,	120,	550.0822963,	2219.930832],
                    [0,	100,	1309.104358,	2219.930832,	0,	222.3969186,	0,	130,	1157.299946,	2371.735244]])
    '''
    for which_action in range(DEFAULT_NUM_OF_ACTION_INTEGRATE):
        flag = True
        for cond in range(DEFAULT_NUM_OF_CONDITION):
            lower = condition[which_action][cond*2]
            upper = condition[which_action][cond*2+1]
            if (lower < compare_list[cond] or lower == DO_NOT_CARE) and (compare_list[cond] < upper or upper == DO_NOT_CARE):
                pass
            else:
                flag = False
        if flag == True:
            result = result + '1'
        else:
            result = result + '0'
    return result

def depict(oil_data,freight_outward_data,freight_homeward_data,exchange_data,demand_data,supply_data,newbuilding_data,secondhand_data,cash_data,pattern,time,ship_number,freight_income_before,decide=True):
    if time == 0:
        cash_data_for_graph = []
        for p in range(pattern+1):
            cash_data_for_graph.append([{'price':0}])
    else:
        cash_data_for_graph = []
        for p in range(pattern+1):
            cash_data_for_graph.append([{'price':0}])
            for i in range(len(cash_data[p])-1):
                for three in range(3):
                    cash_data_for_graph[p].append({'price' : cash_data[p][i+1]['price']})
    x_length = 48
    sns.set()
    sns.set_style('whitegrid')
    sns.set_palette('gray')

    fig = plt.figure()
    list1 = [oil_data,freight_outward_data,freight_homeward_data,exchange_data,demand_data,supply_data,newbuilding_data,secondhand_data,cash_data_for_graph]
    list2 = ([fig.add_subplot(3, 3, 1),fig.add_subplot(3, 3, 2),fig.add_subplot(3, 3, 3),fig.add_subplot(3, 3, 4),
                fig.add_subplot(3, 3, 5),fig.add_subplot(3, 3, 6),fig.add_subplot(3, 3, 7),fig.add_subplot(3, 3, 8),
                fig.add_subplot(3, 3, 9)])
    list3 = ['oil price','freight outward','freight homeward','exchange rate','ship demand','ship supply','new ship','secondhand','cash data']
    list4 = [59.29,1250,810,119.8,10.65,5103,(1+INDIRECT_COST)*66472628.1,(1+INDIRECT_COST)*42139681.02,0]
    list5 = [0,0,500,0,0,0,0,0,-5*10**9]
    list6 = [200,2000,1250,200,200,10000,10*10**7,10*10**7,5*10**9]
    oil_past = [94.62,100.82,100.8,102.07,102.18,105.79,103.59,96.54,93.21,84.4,75.79,59.29]
    outward_past = [2000,1640,1210,1390,1580,1540,1570,1540,1280,1070,1140,1250]
    homeward_past = [820,820,890,850,860,850,840,840,810,850,860,810]
    exchange_past = [102.49,101.66,102.98,102.51,101.64,101.39,102.87,103.83,109.42,111.23,118.22,119.8]
    demand_past = [110.7881933,110.3318198,110.1476691,110.9649126,110.7199579,110.6262684,111.6401227,111.4574122,113.3615791,113.2160901,112.9383983,113.8730479]
    supply_past = [5103]*12
    new_past = [66159183.57,66786072.64,66786072.64,66786072.64,66786072.64,66472628.1,66159183.57,65845739.03,65845739.03,65845739.03,66159183.57,66472628.1]
    second_past = [51464893.07,51464893.07,51464893.07,51464893.07,51464893.07,50946825.74,48874556.39,46025186.04,43693883.03,42916782.02,42398714.69,42139681.02]
    cash_past = [0]*12
    list7 = [oil_past,outward_past,homeward_past,exchange_past,demand_past,supply_past,new_past,second_past,cash_past]
    for (data,ax,name,start,lower,upper,past) in zip(list1,list2,list3,list4,list5,list6,list7):
        if time > x_length-12:
            x,y = [],[]
            for i in range(time-x_length,time):
                x.append(i)
                y.append(data[pattern][i]['price'])
                ax.plot(x,y)
                ax.set_xlim([time-x_length,time])
                if max(y) < upper and min(y) > lower:
                    ax.set_ylim([lower,upper])
                ax.set_title(name)
        else:
            x,y = [],past
            for i in range(-12,0):
                x.append(i)
            for i in range(time+1):
                x.append(i)
                y.append(data[pattern][i]['price'])
                ax.plot(x,y)
                ax.set_xlim([-12,-12+x_length])
                if max(y) < upper and min(y) > lower:
                    ax.set_ylim([lower,upper])
                ax.set_title(name)
    # show plots
    fig.tight_layout()
    fig.suptitle("Market value and your cash in {} months".format(time), fontsize=20)
    plt.subplots_adjust(top=0.80)
    plt.pause(.01)
    if decide:
        average_freight = 0
        if time > 10:
            for i in range(time-10,time):
                average_freight += freight_outward_data[pattern][i]['price']
        else:
            for j in range(0,time+1):
                average_freight += freight_outward_data[pattern][j]['price']
            for k in range(9-time):
                average_freight += outward_past[-k]
        average_freight /= 10
        comparioson = [oil_data,freight_outward_data,freight_homeward_data,exchange_data,demand_data,supply_data,newbuilding_data,secondhand_data]
        comparison_str = []
        if time > 0:
            for compare_data in comparioson:
                if compare_data[pattern][time-3]['price'] > 0:
                    append_data = (compare_data[pattern][time]['price']/compare_data[pattern][time-3]['price'] - 1) * 100
                    comparison_str.append(append_data)
            for index in range(len(comparison_str)):
                if comparison_str[index] > 0:
                    comparison_str[index] = Fore.RED  + '+' +  str(int(comparison_str[index])) + Style.RESET_ALL
                elif comparison_str[index] < 0:
                    comparison_str[index] = Fore.BLUE   +  str(int(comparison_str[index])) + Style.RESET_ALL
        else:
            comparison_str = ['-']*8
        headers = ["oil price", "freight outward","freight homeward"]    
        oil = '{0} ({1}%)  $/barrel'.format(int(oil_data[pattern][time]['price']),comparison_str[0])
        freight_out = '{0} ({1}%)  $/TEU'.format(int(freight_outward_data[pattern][time]['price']),comparison_str[1])
        freight_home = '{0} ({1}%)  $/TEU'.format(int(freight_homeward_data[pattern][time]['price']),comparison_str[2])
        table = [[oil,freight_out,freight_home]]
        result=tabulate(table, headers, tablefmt="grid")
        print(result)
        headers = ["exchange rate","ship demand", "ship supply",]
        exchange = '{0} ({1}%)  yen/$'.format(int(exchange_data[pattern][time]['price']),comparison_str[3])
        demand = '{0} ({1}%)'.format(int(demand_data[pattern][time]['price']),comparison_str[4])
        supply = '{0} ({1}%)  ships'.format(int(supply_data[pattern][time]['price']),comparison_str[5])
        table = [[exchange,demand,supply]]
        result=tabulate(table, headers, tablefmt="grid")
        print(result)
        headers = ["new ship price","secondhand price","cash"]
        new = '{0} ({1}%)  $'.format('{:.2E}'.format(int(newbuilding_data[pattern][time]['price']*1.05)),comparison_str[6])
        second = '{0} ({1}%)  $'.format('{:.2E}'.format(int(secondhand_data[pattern][time]['price']*1.05)),comparison_str[7])
        ca = '{0}  $'.format('{:.2E}'.format(int(cash_data_for_graph[pattern][time]['price'])))
        table = [[new,second,ca]]
        result=tabulate(table, headers, tablefmt="grid")
        print(result)
        headers = ["freight income last three month","average freight outward past ten months"]
        freight_income_last_three_month = '{}  $'.format('{:.2E}'.format(int(freight_income_before)))
        average_freight = '{}  $/TEU'.format(int(average_freight))
        table = [[freight_income_last_three_month,average_freight]]
        result=tabulate(table, headers, tablefmt="grid")
        print(result)
        s0 = 'please enter one decision among 000 to 111'
        print(Fore.BLACK + Back.LIGHTYELLOW_EX +s0+Style.RESET_ALL)
        if time == 0:
            print('000 means that order 0 new ship and buy 0 secondhand ship and sell 0 ship')
            print('111 means that order 1 new ship and buy 1 secondhand ship and sell 1 ship')
            print('xyz means that order x new ship and buy y secondhand ship and sell z ship')
            print('you can enter only 0 or 1 in x,y,z.')
        flag = True
        error = False
        while flag:
            if error:
                print('You can enter only 000 to 111')
            input_line = input()
            if input_line == '000' or input_line == '001' or input_line == '010' or input_line == '011' or input_line == '100' or input_line == '101' or input_line == '110' or input_line == '111': 
                result = input_line
                flag = False
            else:
                error = True
    else:
        print('if you has checked your cash data, enter')
        input_line = input()
        result = ''
    plt.close()
    return result

def read_csv_data():
    decision_csv = [[],[],[]]
    path = '../../experiment result/decisions/okubo.csv'
    with open(path) as f:
        reader = csv.reader(f)
        flag = 0
        for row in reader:
            if flag > 0:
                if row[0] != '':
                    for i in range(3):
                        if len(row[i]) == 1:
                            decision_csv[i].append('00'+row[i])
                        elif len(row[i]) == 2:
                            decision_csv[i].append('0'+row[i])
                        elif len(row[i]) == 3:
                            decision_csv[i].append(row[i])   
                        else: 
                            decision_csv[i].append(row[i][1:4])
            flag += 1
    return decision_csv


def fitness_function(oil_data,freight_outward_data,freight_homeward_data,exchange_data,demand_data,supply_data,newbuilding_data,secondhand_data):
    Record = []
    cash_data = []
    cash_in_yen_data = []
    #decision_csv = read_csv_data()
    for pattern in range(3):
        fitness = 0
        ship = Ship(TEU_SIZE,INITIAL_SPEED,ROUTE_DISTANCE)
        cash_data.append([{'price':0}])
        cash_in_yen_data.append([0])
        decision_data = ['']
        month_data = [0]
        cash_in_yen = 0
        #decision_number = 0
        freight_income = 0
        for year in range(DEFAULT_PREDICT_YEARS):
            cash_flow = 0
            if year >= PAYBACK_PERIOD and ship.exist_number + ship.order_number <= 0:
                    break
            for month in range(0,12,TIME_STEP):
                time = year*12+month
                current_oil_price = oil_data[pattern][time]['price']
                current_freight_rate_outward = freight_outward_data[pattern][time]['price']
                current_freight_rate_return = freight_homeward_data[pattern][time]['price']
                total_freight = ( current_freight_rate_outward * LOAD_FACTOR_ASIA_TO_EUROPE + current_freight_rate_return * LOAD_FACTOR_EUROPE_TO_ASIA)
                current_exchange = exchange_data[pattern][time]['price']
                current_demand = demand_data[pattern][time]['price']
                current_supply = supply_data[pattern][time]['price']
                ship_number = ship.exist_number+ship.order_number
                if year < PAYBACK_PERIOD:
                    current_newbuilding = newbuilding_data[pattern][time]['price']
                    current_secondhand = secondhand_data[pattern][time]['price']
                    #print()
                    if withRule:
                        recomend = adapt_rule(current_oil_price,current_freight_rate_outward,current_exchange,ship.exist_number+ship.order_number,freight_outward_data[pattern],year*12+month)
                        print(Fore.RED + 'The action rule recommends is {}'.format(recomend) + Style.RESET_ALL)
                    #print('Now your company own {} ships'.format(Fore.BLUE + str(ship.exist_number+ship.order_number) + Style.RESET_ALL))
                    #decisions = depict(oil_data,freight_outward_data,freight_homeward_data,exchange_data,demand_data,supply_data,newbuilding_data,secondhand_data,cash_data,pattern,time,ship_number,freight_income)
                    #decisions = adapt_rule(current_oil_price,current_freight_rate_outward,current_exchange,ship.exist_number+ship.order_number,freight_outward_data[pattern],year*12+month)
                    #decisions = decision_csv[pattern][decision_number]
                    #decision_number += 1
                    decisions = str(random.randint(0,1)) + str(random.randint(0,1)) + str(random.randint(0,1))
                    answer = adapt_rule(current_oil_price,current_freight_rate_outward,current_exchange,ship.exist_number+ship.order_number,freight_outward_data[pattern],year*12+month)
                    if int(decisions[0]) == 1:
                        cash_flow += ship.buy_new_ship(newbuilding_data[pattern][time]['price'],int(decisions[0])) 
                    if int(decisions[1]) == 1:
                        cash_flow += ship.buy_secondhand_ship(secondhand_data[pattern][time]['price'],int(decisions[1]))
                    if int(decisions[2]) == 1:
                        cash_flow += ship.sell_ship(secondhand_data[pattern][time]['price'],int(decisions[2]))
                freight_income = ship.calculate_income_per_time_step_month(current_oil_price,total_freight,current_demand,current_supply)
                cash_flow += freight_income
                cash_flow += ship.add_age()
                if year == 0:
                    cash_data[pattern].append({'price':0 + cash_flow/((1 + DISCOUNT_RATE) ** (year + 1))})
                    cash_in_yen_data[pattern].append(0)
                else:
                    cash_data[pattern].append({'price':cash_data[pattern][int(year*12/TIME_STEP)]['price'] + cash_flow/((1 + DISCOUNT_RATE) ** (year + 1))})
                    cash_in_yen_data[pattern].append(cash_in_yen_data[pattern][int(year*12/TIME_STEP)])
                month_data.append(year*12+month)
                if year < PAYBACK_PERIOD:
                    if answer == decisions:
                        decision_data.append('T' + decisions)
                    else:
                        decision_data.append('F' + decisions + ',' + answer)
                else:
                    decision_data.append('')
            cash_in_yen += exchange_data[pattern][year*12+11]['price']*(cash_flow/((1 + DISCOUNT_RATE) ** (year + 1)))
            s = 'NOW YOUR CASH IS {} MILLION YEN'.format(int(cash_in_yen/1000000))
            #print(Fore.GREEN + s + Style.RESET_ALL)
            cash_in_yen_data[pattern][-1] = cash_in_yen
            DISCOUNT = (1 + DISCOUNT_RATE) ** (year + 1)
            cash_flow *= exchange_data[pattern][year*12+11]['price']
            fitness += cash_flow / DISCOUNT
        fitness /= HUNDRED_MILLION# one hundred millon JPY
        Record.append(fitness)
        export(pattern,month_data,decision_data,cash_data[pattern],cash_in_yen_data[pattern])
        '''
        print('if you are ready to continue, enter yes')
        flag = True
        while flag:
            input_line = input()
            if input_line == 'yes': 
                flag = False
                print('next one is pattern {}'.format(pattern+1))
                print()
                print()
                print()
        '''
    e, sigma = calc_statistics(Record)
    return [e,sigma]

def main():
    oil_data,freight_outward_data,freight_homeward_data,exchange_data,demand_data,supply_data,newbuilding_data,secondhand_data = load_generated_sinario()
    score = []
    simulation_number = 100000
    for i in range(simulation_number):
        e,sigma = fitness_function(oil_data,freight_outward_data,freight_homeward_data,exchange_data,demand_data,supply_data,newbuilding_data,secondhand_data)
        score.append(e)
    #print(score)
    print('average profit = ','{:.3E}'.format(int(sum(score)*HUNDRED_MILLION/simulation_number)))
    print('The simulation is over.')
    print('Thank you for your cooperation')

def export(pattern,month_data,decision_data,cash_data,cash_in_yen_data):
    p = 'pattern{}'.format(pattern)
    path = '../output/{}.csv'.format(p)
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['month', 'decision','cash in yen','cash in dollar'])
    with open(path, 'a') as f:
        writer = csv.writer(f)
        for time in range(len(month_data)):
            row = []
            row.append(month_data[time])
            row.append(decision_data[time])
            row.append(cash_data[time]['price'])
            row.append(cash_in_yen_data[time])
            writer.writerow(row)
    
if __name__ == "__main__":
    main()
