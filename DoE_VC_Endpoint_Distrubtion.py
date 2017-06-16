import glob
import re

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

graph_interval_speed = 250


# Import filenames
files = glob.glob('.\BUD_Data\*')

# Create placeholder DataFrame
init_df = pd.DataFrame(columns=['SITE TYPE', 'DATE', 'MAKE', 'MODEL', 'COUNTER'], )

# Import data from files
for file in files:
    filename = re.search('.*BUD_Data\\\(.*)', file).group(1)
    date_id = pd.to_datetime(filename[0:8])

    temp_df = pd.DataFrame()

    try:
        temp_df = pd.read_csv(file, header=3)
    except:
        print("File formats need to be in CSV.")

    temp_df['DATE'] = date_id
    temp_df['COUNTER'] = 1

    # Exclude BER and CCP
    # temp_df_filter = ~temp_df['SYSTEM NAME'].astype('str').str.contains('- P21|- SLC|- CC')
    # temp_df = temp_df[temp_df_filter]

    # Minimising of columns required
    temp_df = temp_df[['DATE', 'SITE TYPE', 'MAKE', 'MODEL', 'COUNTER']]

    # Cleaning of Data
    temp_df.replace(to_replace=['TAFE Sites', 'TAFE Institute Offices'], value='TAFE', inplace=True)
    temp_df.replace(to_replace=['External School Sites', 'School Sites', 'Tutorial Centre'], value='School',
                    inplace=True)
    temp_df.replace(to_replace=['Industry Training Centres', 'External Organisations'], value='Other', inplace=True)
    temp_df.replace(to_replace=['School Group Office Building', 'State Offices', 'Regional Offices',
                                'Departmental Offices', 'School Group Office'], value='Corporate', inplace=True)
    temp_df.replace(to_replace=['v700', 'V700', ' V700', 'V700 (128)', ' V700 (128)', 'V700 (64)', 'V 700 (128)'],
                    value='V 700', inplace=True)
    temp_df.replace(to_replace=['VSX 3000A (64)', 'VSX 3000A (128)'], value='VSX 3000A', inplace=True)
    temp_df.replace(to_replace=['VSX 5000 (128)'], value='VSX 5000', inplace=True)
    temp_df.replace(to_replace=['VSX 6000 (128)', 'VSX 6000 (64)', ' VSX 6000 (64) ', ' VSX 6000 (64)', 'VSX6000',
                                'VSX 6000 (64) ', 'VSX 6000 '], value='VSX 6000', inplace=True)
    temp_df.replace(to_replace=['VSX7000', 'VSX 7000 (128)', 'VSX 7000 (64)'], value='VSX 7000', inplace=True)
    temp_df.replace(to_replace=['VSX7000A', 'VSX 7000A (128)', 'VSX7000s'], value='VSX 7000A', inplace=True)
    temp_df.replace(to_replace=['VSX 7000E (128)', 'VSX 7000e (128)', 'VSX 7000e'], value='VSX 7000E', inplace=True)
    temp_df.replace(to_replace=['VSX 8000 (128)'], value='VSX 8000', inplace=True)
    temp_df.replace(to_replace=['HDX 7000 HD'], value='HDX 7000', inplace=True)
    temp_df.replace(to_replace=['HDX 4000 ', 'HDX4000', 'HSX 4000 HD', 'HDX 4000 HD'], value='HDX 4000', inplace=True)
    temp_df.replace(to_replace=['HDX 8000b HD', 'HDX8000', 'HDX 8000 HD'], value='HDX 8000', inplace=True)
    temp_df.replace(to_replace=['HDX6000 HD', 'HDX 6000HD', 'HDX 6000 HD', 'HDX6000'], value='HDX 6000', inplace=True)
    temp_df.replace(to_replace=['4500 HDX', 'HDX 4500 HD', 'HD 4500', 'HDX 4500 ', 'HD 4500 HD'],
                    value='HDX 4500', inplace=True)
    temp_df.replace(to_replace=['HDX 9006 '], value='HDX 9006', inplace=True)
    temp_df.replace(to_replace=['RealPresence Group 310'], value='GS 310', inplace=True)
    temp_df.replace(to_replace=['RealPresence Group 500'], value='GS 500', inplace=True)
    temp_df.replace(to_replace=['300 MXP', '3000 MXP', '3000 MXP ', '3000MXP'], value='MXP 3000', inplace=True)
    temp_df.replace(to_replace=['17000 MXP', '1700 MXP'], value='MXP 1700', inplace=True)
    temp_df.replace(to_replace=['1000 MXP'], value='MXP 1000', inplace=True)
    temp_df.replace(to_replace=['990MXP', '990 MPX', '990 MXP'], value='MXP 990', inplace=True)
    temp_df.replace(to_replace=['Cisco C40', 'C40  ', 'C40'], value='C 40', inplace=True)
    temp_df.replace(to_replace=['C20'], value='C 20', inplace=True)
    temp_df.replace(to_replace=['CISCO EX60', 'Cisco EX60', 'EX60  ', 'EX60 ', 'EX60'], value='EX 60', inplace=True)
    temp_df.replace(to_replace=['Cisco SX20', 'SX20'], value='SX 20', inplace=True)
    temp_df.replace(to_replace=['SX80'], value='SX 80', inplace=True)
    temp_df.replace(to_replace=['TANDBERG', 'Tanberg', 'Tandberg ', 'Tandberg'], value='Cisco', inplace=True)
    temp_df.replace(to_replace=['CISCO', 'Cisco Systems'], value='Cisco', inplace=True)
    temp_df.replace(to_replace=['Polycom ', 'Tamworth STC Reg Mgr Ofc'], value='Polycom', inplace=True)

    temp_df.loc[(temp_df['MODEL'] == 'HDX 4000') & (temp_df['MAKE'] == 'Cisco'), ['MAKE']] = 'Polycom'

    # Counts based on SITE TYPE, DATE, MAKE, MODEL
    temp_df = pd.pivot_table(temp_df, index=['SITE TYPE', 'DATE', 'MAKE', 'MODEL'], aggfunc='count').reset_index()

    # Data appended to common set
    init_df = init_df.append(temp_df)

# Group into monthly frequency based on max value
main_df = init_df.groupby(['SITE TYPE', pd.Grouper(freq='M', key='DATE'), 'MAKE', 'MODEL']).max().reset_index()
main_df = pd.pivot_table(main_df, index=['DATE', 'SITE TYPE'], columns=['MAKE', 'MODEL'])
main_df.columns = main_df.columns.droplevel()
main_df.reset_index(inplace=True)
main_df = pd.melt(main_df, id_vars=['DATE', 'SITE TYPE'], var_name=['MAKE', 'MODEL'], value_name='COUNTER')
main_df.sort_values(by=['DATE', 'SITE TYPE', 'MAKE', 'MODEL'])
main_df.set_index('DATE', inplace=True)

# Fill in blanks with 0 as all blanks are 0 devices counted
main_df.fillna(0, inplace=True)


# This bit and the MONKEY PATCH were stole from to get title changes working
# https://stackoverflow.com/questions/17558096/animated-title-in-matplotlib/17562747#17562747

def _blit_draw(self, artists, bg_cache):
    # Handles blitted drawing, which renders only the artists given instead
    # of the entire figure.
    updated_ax = []
    for a in artists:
        # If we haven't cached the background for this axes object, do
        # so now. This might not always be reliable, but it's an attempt
        # to automate the process.
        if a.axes not in bg_cache:
            # bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.axes.bbox)
            # change here
            bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.axes.figure.bbox)
        a.axes.draw_artist(a)
        updated_ax.append(a.axes)

    # After rendering all the needed artists, blit each axes individually.
    for ax in set(updated_ax):
        # and here
        # ax.figure.canvas.blit(ax.bbox)
        ax.figure.canvas.blit(ax.figure.bbox)


# MONKEY PATCH!!
animation.Animation._blit_draw = _blit_draw

# Collective Figure
# Collect DataSets
# Common Data
c_pause = False
c_date_range = pd.to_datetime(main_df.reset_index()['DATE'].unique()).tolist()

# Model Distribution Data
c_m_models = main_df.sort_values(['MAKE', 'MODEL'])['MODEL'].unique()
c_m_total_df = main_df.reset_index().groupby(['DATE', 'MAKE', 'MODEL']).sum().reset_index(). \
    sort_values(['DATE', 'MAKE', 'MODEL']).set_index('DATE')
c_m_corporate_df = main_df[main_df['SITE TYPE'] == 'Corporate'].reset_index(). \
    sort_values(['DATE', 'MAKE', 'MODEL']).set_index('DATE')
c_m_school_df = main_df[main_df['SITE TYPE'] == 'School'].reset_index(). \
    sort_values(['DATE', 'MAKE', 'MODEL']).set_index('DATE')
c_m_tafe_df = main_df[main_df['SITE TYPE'] == 'TAFE'].reset_index(). \
    sort_values(['DATE', 'MAKE', 'MODEL']).set_index('DATE')
c_m_other_df = main_df[main_df['SITE TYPE'] == 'Other'].reset_index(). \
    sort_values(['DATE', 'MAKE', 'MODEL']).set_index('DATE')
c_m_max_y = c_m_total_df['COUNTER'].max()
c_m_max_x = len(c_m_models)

# Vendor Distribution Data
vendor_df = main_df.reset_index().groupby(['DATE', 'SITE TYPE', 'MAKE']).sum().reset_index()
vendor_df.set_index('DATE', inplace=True)
c_v_total_df = main_df.reset_index().groupby(['DATE', 'MAKE']).sum().reset_index(). \
    sort_values(['DATE', 'MAKE']).set_index('DATE')
c_v_corporate_df = vendor_df[vendor_df['SITE TYPE'] == 'Corporate'].reset_index(). \
    sort_values(['DATE', 'MAKE']).set_index('DATE')
c_v_school_df = vendor_df[vendor_df['SITE TYPE'] == 'School'].reset_index(). \
    sort_values(['DATE', 'MAKE']).set_index('DATE')
c_v_tafe_df = vendor_df[vendor_df['SITE TYPE'] == 'TAFE'].reset_index(). \
    sort_values(['DATE', 'MAKE']).set_index('DATE')
c_v_other_df = vendor_df[vendor_df['SITE TYPE'] == 'Other'].reset_index(). \
    sort_values(['DATE', 'MAKE']).set_index('DATE')
c_v_max_y = c_v_total_df['COUNTER'].max()
c_v_max_x = 2

# Figure Creation
c_fig = plt.figure()


# Model Plot
c_m_fig_ax = c_fig.add_subplot(121)
c_m_fig_ax.set_xlim((0, c_m_max_x - 1))
c_m_fig_ax.set_ylim((0, c_m_max_y))
c_m_fig_ax.set_xlabel('Models')
c_m_fig_ax.set_ylabel('# of Endpoints')
plt.xticks(range(len(c_m_models)), c_m_models, rotation=70)
c_m_ttl = c_m_fig_ax.text(.5, 1.05, '', transform=c_m_fig_ax.transAxes, va='center')

# Lines
c_m_line_total, = c_m_fig_ax.plot([], [], lw=2, label='Total', alpha=0.5, ls='--')
c_m_line_corp, = c_m_fig_ax.plot([], [], lw=1, label='Corporate', alpha=0.5)
c_m_line_school, = c_m_fig_ax.plot([], [], lw=1, label='School', alpha=0.5)
c_m_line_tafe, = c_m_fig_ax.plot([], [], lw=1, label='TAFE', alpha=0.5)
c_m_line_other, = c_m_fig_ax.plot([], [], lw=1, label='Other', alpha=0.5)
c_m_fig_ax.legend(loc='upper right')

# Vendor Plot
c_v_fig_ax = c_fig.add_subplot(122)
plt.xticks(range(2), ['Cisco', 'Polycom'], rotation=70)

c_v_fig_ax.set_xlim((0, c_v_max_x - 1))
c_v_fig_ax.set_ylim((0, c_v_max_y))
c_v_fig_ax.set_xlabel('Vendors')
c_v_fig_ax.set_ylabel('# of Endpoints')

c_v_ttl = c_v_fig_ax.text(.5, 1.05, '', transform=c_v_fig_ax.transAxes, va='center')

# Lines
c_v_line_total, = c_v_fig_ax.plot([], [], lw=2, label='Total', alpha=0.5, ls='--')
c_v_line_corp, = c_v_fig_ax.plot([], [], lw=1, label='Corporate', alpha=0.5)
c_v_line_school, = c_v_fig_ax.plot([], [], lw=1, label='School', alpha=0.5)
c_v_line_tafe, = c_v_fig_ax.plot([], [], lw=1, label='TAFE', alpha=0.5)
c_v_line_other, = c_v_fig_ax.plot([], [], lw=1, label='Other', alpha=0.5)
c_v_fig_ax.legend(loc='upper right')


def c_init():
    c_m_ttl.set_text('')
    c_m_line_total.set_data([], [])
    c_m_line_corp.set_data([], [])
    c_m_line_school.set_data([], [])
    c_m_line_tafe.set_data([], [])
    c_m_line_other.set_data([], [])
    c_v_ttl.set_text('')
    c_v_line_total.set_data([], [])
    c_v_line_corp.set_data([], [])
    c_v_line_school.set_data([], [])
    c_v_line_tafe.set_data([], [])
    c_v_line_other.set_data([], [])

    return c_m_ttl, c_m_line_total, c_m_line_corp, c_m_line_school, c_m_line_tafe, c_m_line_other, \
        c_v_ttl, c_v_line_total, c_v_line_corp, c_v_line_school, c_v_line_tafe, c_v_line_other


def c_animate(i):
    if not c_pause:
        c_m_ttl.set_text('VC EP Model Distribution for {}'.format(str(c_date_range[i])[:7]))
        m_x_total = range(len(c_m_total_df.loc[c_date_range[i]]['MODEL'].tolist()))
        m_y_total = c_m_total_df.loc[c_date_range[i]]['COUNTER'].tolist()
        m_x_corporate = range(len(c_m_corporate_df.loc[c_date_range[i]]['MODEL'].tolist()))
        m_y_corporate = c_m_corporate_df.loc[c_date_range[i]]['COUNTER'].tolist()
        m_x_school = range(len(c_m_school_df.loc[c_date_range[i]]['MODEL'].tolist()))
        m_y_school = c_m_school_df.loc[c_date_range[i]]['COUNTER'].tolist()
        m_x_tafe = range(len(c_m_tafe_df.loc[c_date_range[i]]['MODEL'].tolist()))
        m_y_tafe = c_m_tafe_df.loc[c_date_range[i]]['COUNTER'].tolist()
        m_x_other = range(len(c_m_other_df.loc[c_date_range[i]]['MODEL'].tolist()))
        m_y_other = c_m_other_df.loc[c_date_range[i]]['COUNTER'].tolist()
        c_m_line_total.set_data(m_x_total, m_y_total)
        c_m_line_corp.set_data(m_x_corporate, m_y_corporate)
        c_m_line_school.set_data(m_x_school, m_y_school)
        c_m_line_tafe.set_data(m_x_tafe, m_y_tafe)
        c_m_line_other.set_data(m_x_other, m_y_other)
        c_v_ttl.set_text('VC EP Vendor Distribution for {}'.format(str(c_date_range[i])[:7]))
        v_x_total = range(len(c_v_total_df.loc[c_date_range[i]]['MAKE'].tolist()))
        v_y_total = c_v_total_df.loc[c_date_range[i]]['COUNTER'].tolist()
        v_x_corporate = range(len(c_v_corporate_df.loc[c_date_range[i]]['MAKE'].tolist()))
        v_y_corporate = c_v_corporate_df.loc[c_date_range[i]]['COUNTER'].tolist()
        v_x_school = range(len(c_v_school_df.loc[c_date_range[i]]['MAKE'].tolist()))
        v_y_school = c_v_school_df.loc[c_date_range[i]]['COUNTER'].tolist()
        v_x_tafe = range(len(c_v_tafe_df.loc[c_date_range[i]]['MAKE'].tolist()))
        v_y_tafe = c_v_tafe_df.loc[c_date_range[i]]['COUNTER'].tolist()
        v_x_other = range(len(c_v_other_df.loc[c_date_range[i]]['MAKE'].tolist()))
        v_y_other = c_v_other_df.loc[c_date_range[i]]['COUNTER'].tolist()
        c_v_line_total.set_data(v_x_total, v_y_total)
        c_v_line_corp.set_data(v_x_corporate, v_y_corporate)
        c_v_line_school.set_data(v_x_school, v_y_school)
        c_v_line_tafe.set_data(v_x_tafe, v_y_tafe)
        c_v_line_other.set_data(v_x_other, v_y_other)

    return c_m_ttl, c_m_line_total, c_m_line_corp, c_m_line_school, c_m_line_tafe, c_m_line_other, \
        c_v_ttl, c_v_line_total, c_v_line_corp, c_v_line_school, c_v_line_tafe, c_v_line_other


def c_on_click(_):
    global c_pause
    c_pause ^= True


c_fig.canvas.mpl_connect('button_press_event', c_on_click)

c_anim = animation.FuncAnimation(c_fig, c_animate, init_func=c_init, repeat=True,
                                 frames=len(c_date_range),
                                 interval=graph_interval_speed, blit=True)

# Save Video of Animated Plot
# Set values for ffmpeg application
c_fig.set_size_inches(16, 11)
plt.rcParams['animation.ffmpeg_path'] = '.\\FFMPEG\\bin\\ffmpeg.exe'
plt.rcParams['animation.bitrate'] = 1000



# Create video writer
# FFwriter = animation.FFMpegWriter(fps=10, extra_args=['-s', '1080:1920', '-aspect', '16:9'])
#
# # Trigger saving of animation to video
# print("Creating Video File")
# c_anim.save('VC_Endpoint_Distribution-2008_2017-10FPS.mp4', writer=FFwriter, dpi=600)
#
# print("Animation Video Created")

# Display Figure
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.show()

# Write to csv file after pivot
# comp_new = pd.pivot_table(comp_new, index=['DATE', 'SITE TYPE', 'MAKE', 'MODEL'], columns=['COUNTER'])
# comp_new.to_csv('output.csv')
