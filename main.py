import pandas as pd
import os
import matplotlib.pyplot as plt
from PIL import Image
import warnings

warnings.filterwarnings("ignore")


def team_colours(col):
    primary_colour = {
        "Argentina": "#43A1D5",
        "Australia": "#FFCD00",
        "Belgium": "#E30613",
        "Brazil": "#FFDC02",
        "Cameroon": "#479A50",
        "Canada": "#C5281C",
        "Costa Rica": "#EC1D25",
        "Croatia": "#ED1C24",
        "Denmark": "#C60C30",
        "Ecuador": "#FFCE00",
        "England": "#FFFFFF",
        "France": "#21304D",
        "Germany": "#000000",
        "Ghana": "#FFFFFF",
        "Iran": '#FFFFFF',
        "Japan": "#000555",
        "Mexico": "#00933B",
        "Morocco": "#E50011",
        "Netherlands": "#F36C21",
        "Poland": "#FFFFFF",
        "Portugal": "#E42518",
        "Qatar": "#7F1431",
        "Saudi Arabia": "#125B34",
        "Senegal": "#FFFFFF",
        "Serbia": "#B72E3E",
        "South Korea": "#EC0F32",
        "Spain": "#8B0D11",
        "Switzerland": "#D52B1E",
        "Tunisia": "#FFFFFF",
        "Uruguay": "#55B5E5",
        "Wales": "#AE2630",
        "USA": "#FFFFFF"}

    clr = []
    for team in col:
        if team in primary_colour:
            clr.append(primary_colour[team])
        else:
            print(team)
    return clr

def get_csvs():
    df_list = []
    csvs_folder = 'csvs'
    csvs_list = os.listdir(csvs_folder)
    
    for csv_file in csvs_list:
        if csv_file[-3:] == 'csv':
            df = pd.read_csv(os.path.join(csvs_folder, csv_file), sep='\t', header=[0])
            country_name = csv_file[0:-4].replace('_', ' ')
            country_name = country_name.title()
            if country_name == 'Usa':
                country_name = 'USA'
                
            df['Country'] = country_name
            df[['Club','Club Nation']] = df.Club.str.split('(', expand=True)
            df['Club Nation'] = df['Club Nation'].str.replace(')','')
            df['Club Nation'] = df['Club Nation'].str.replace(' ','')
            df_list.append(df)

    return df_list

def annotations(ax):
    ax.annotate('Data from sportingnews.com', (0,0), (0,-40), fontsize=12, 
                xycoords='axes fraction', textcoords='offset points', va='top', color='navajowhite')
    ax.annotate('Data Viz by Andreas Calleja @andreascalleja', (0,0), (0,-60), fontsize=12,
                xycoords='axes fraction', textcoords='offset points', va='top', color='navajowhite')
    ax.annotate('Data correct as of squad announcements', (0,0), (0,-80), fontsize=12, 
                xycoords='axes fraction', textcoords='offset points', va='top', color='navajowhite')


def get_age(df_list):
    df_age = pd.DataFrame(columns=['Country','Age'])
    for df in df_list:
        country = df.iloc[0, df.columns.get_loc('Country')]
        age = round(df["Age"].mean(), 2)
        row = {'Country': country, 'Age': age}
        concat_df = pd.DataFrame([row])
        df_age = pd.concat([df_age, concat_df], ignore_index=True)
    
    return df_age.sort_values(by=['Age'])


def get_total(df_list, column_name):
    df_total = pd.DataFrame(columns=['Country', column_name])
    for df in df_list:
        country = df.iloc[0, df.columns.get_loc('Country')]
        total = df[column_name].sum()
        row = {'Country': country, column_name: total}
        concat_df = pd.DataFrame([row])
        df_total = pd.concat([df_total, concat_df], ignore_index=True)
    
    return df_total.sort_values(by=[column_name])


def get_age_plot(df, filename):
    fig = plt.figure(figsize=(25,22), dpi=300, tight_layout=True)
    fig.patch.set_facecolor('dimgray')
    
    ax = fig.add_subplot()
    ax.set_facecolor('dimgray')
    ax.set_title('Average Age of World Cup Squads', size=32, color='darkorange', pad=-20)
    ax.set_xlabel('Average Squad Age', size=18, color='darkorange')
    ax.set_ylabel('Countries', size=18, color='darkorange')
    
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
        
    bars = ax.barh(df["Country"], df["Age"], color=team_colours(df["Country"]), height=0.75, align='center')
    ax.bar_label(bars, size=16, color='darkorange')
    ax.axis(xmin=24, xmax=29)
    ax.grid(False)
        
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14)
        label.set_color('navajowhite')
        
    fig.subplots_adjust(top=0.8)
    
    max_age = df.loc[df['Age'].idxmax()]
    min_age = df.loc[df['Age'].idxmin()]
    
    textstr = '\n'.join((
        f'Oldest Squad: {max_age["Country"]}. Average Age: {max_age["Age"]:.2f}',
        f'\n',
        f'Youngest Squad: {min_age["Country"]}. Average Age: {min_age["Age"]:.2f}'))
        
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.65, 0.5, textstr, transform=ax.transAxes, fontsize=25,
        verticalalignment='top', bbox=props)
        
    annotations(ax)
                
    fig.savefig(f'figures/{filename}.png', bbox_inches='tight')


def get_total_plot(df, column_name, filename):
    fig = plt.figure(figsize=(25,22), dpi=300, tight_layout=True)
    fig.patch.set_facecolor('dimgray')
    
    ax = fig.add_subplot()
    ax.set_facecolor('dimgray')
    ax.set_title(f'Total International {column_name} of World Cup Squads', size=32, color='darkorange', pad=-20)
    ax.set_xlabel(f'Total International {column_name}', size=18, color='darkorange')
    ax.set_ylabel('Countries', size=18, color='darkorange')
    
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
        
    bars = ax.barh(df["Country"], df[column_name], color=team_colours(df["Country"]), height=0.75, align='center')
    ax.bar_label(bars, size=16, color='darkorange')
    ax.grid(False)
        
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14)
        label.set_color('navajowhite')

    
        
    fig.subplots_adjust(top=0.8)
    
    # textstr = '\n'.join((
    #     f'Oldest Squad: {max_age["Country"]}. Average Age: {max_age["Age"]:.2f}',
    #     f'\n',
    #     f'Youngest Squad: {min_age["Country"]}. Average Age: {min_age["Age"]:.2f}'))
        
    # props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # ax.text(0.65, 0.5, textstr, transform=ax.transAxes, fontsize=25,
    #     verticalalignment='top', bbox=props)

    annotations(ax)
        
    
                
    fig.savefig(f'figures/{filename}.png', bbox_inches='tight')


def overlay_logo(filename):
    img1 = Image.open(f'figures/{filename}.png')
    width1, height1 = img1.size
    
    img2 = Image.open('logo/world_cup_logo.png')
    img2 = img2.resize((1500, 1793))
    
    img1.paste(img2, (int(width1*0.7), int(height1*0.6)), mask = img2)
    img1.save(f'figures/{filename}_logo.png')


def main():
    df_list = get_csvs()
    df_age = get_age(df_list)
    get_age_plot(df_age, 'world_cup_average_age')
    overlay_logo('world_cup_average_age')
    for column_name in ['Caps', 'Goals']:
        df = get_total(df_list, column_name)
        get_total_plot(df, column_name, f'world_cup_total_{column_name.lower()}')
        overlay_logo(f'world_cup_total_{column_name.lower()}')

    # Retrieve most capped player and number of players with 0 caps


main()
