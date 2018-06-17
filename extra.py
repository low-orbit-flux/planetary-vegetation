
def plot_data(data_file, graph_outpout_file, start_date, stop_date ):
    gnuplot_script = ' '.join((
    "set title \"Followers over time\"\n",
    "set xlabel \"Date / Time\"\n",
    "set ylabel \"Followers\"\n",
    "set term png\n",
    "set output \"" + graph_outpout_file + "\"\n",
    "set xdata time\n",
    "set timefmt \"%Y-%m-%d %H:%M:%S\"\n",
    "set format x \"%m-%d\"\n",
    "set xrange [\"" + start_date + "\":\"" + stop_date + "\"] \n",
    "set datafile separator \",\"\n",
    "set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb\"#483D8B\" behind\n",
    "plot '" + data_file + "' using 1:2 with lines linecolor rgb \"#00FF00\" \n"
    ))
    f = open('gnuplot_script_tmp.txt', 'w')
    f.write(gnuplot_script)
    f.close()
    p = subprocess.Popen("gnuplot gnuplot_script_tmp.txt", shell = True)
    os.waitpid(p.pid, 0)
    os.remove('gnuplot_script_tmp.txt')


def graph_followers(data_file, report_file, graph_outpout_file, acct_id):
    cursor.execute("SELECT twitter_metrics.date, twitter_accounts.first_name, twitter_accounts.last_name, twitter_metrics.following, twitter_metrics.followers from twitter_accounts LEFT JOIN twitter_metrics ON twitter_metrics.twitter_acct=twitter_accounts.ID where twitter_accounts.ID=" + str(acct_id))
    results = []
    f = open(data_file, 'w')
    for i in cursor:
        results.append(i)
        f.write(str(i[0]) + "," + i[4] + "\n")
    f.close()
    f = open(report_file, 'a')
    f.write( "<h1>" + results[-1][1] + " " + results[-1][2] + "</h1>" )
    f.write( "Following: " + results[-1][3] + "<br>")
    f.write( "Followers: <b>" + results[-1][4] + "</b><br>" )
    f.write( "<img src=\"" + graph_outpout_file + "\" >" )
    f.close()