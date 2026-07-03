using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Text;

class Program
{
    static void Main()
    {
        try
        {
            string exeDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            string pyzPath = Path.Combine(exeDir, "OpenXterm.pyz");
            if (!File.Exists(pyzPath))
                pyzPath = Path.Combine(Directory.GetCurrentDirectory(), "OpenXterm.pyz");

            if (!File.Exists(pyzPath))
            {
                System.Windows.Forms.MessageBox.Show(
                    "找不到 OpenXterm.pyz，请确保它与本程序在同一目录下。",
                    "OpenXterm", 
                    System.Windows.Forms.MessageBoxButtons.OK, 
                    System.Windows.Forms.MessageBoxIcon.Error);
                return;
            }

            string pythonw = FindPythonw();
            if (pythonw == null)
            {
                System.Windows.Forms.MessageBox.Show(
                    "找不到 pythonw.exe，请确保已安装 Python 3。",
                    "OpenXterm",
                    System.Windows.Forms.MessageBoxButtons.OK,
                    System.Windows.Forms.MessageBoxIcon.Error);
                return;
            }

            Process.Start(new ProcessStartInfo
            {
                FileName = pythonw,
                Arguments = "\"" + pyzPath + "\"",
                WorkingDirectory = exeDir,
                UseShellExecute = false,
                CreateNoWindow = true
            });
        }
        catch (Exception ex)
        {
            try
            {
                System.Windows.Forms.MessageBox.Show(
                    "启动失败: " + ex.Message,
                    "OpenXterm",
                    System.Windows.Forms.MessageBoxButtons.OK,
                    System.Windows.Forms.MessageBoxIcon.Error);
            }
            catch { }
        }
    }

    static string FindPythonw()
    {
        // Search PATH directly
        string pathEnv = Environment.GetEnvironmentVariable("PATH");
        if (pathEnv != null)
        {
            foreach (string dir in pathEnv.Split(';'))
            {
                try
                {
                    string test = Path.Combine(dir.Trim(), "pythonw.exe");
                    if (File.Exists(test))
                        return test;
                }
                catch { }
            }
        }

        // Common install locations
        string localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        string[] searchDirs = {
            Path.Combine(localAppData, "Programs", "Python"),
            Path.Combine(localAppData, "Programs", "Python", "Python313"),
            Path.Combine(localAppData, "Programs", "Python", "Python312"),
            Path.Combine(localAppData, "Programs", "Python", "Python311"),
            Path.Combine(localAppData, "Programs", "Python", "Python310"),
            @"C:\Python313",
            @"C:\Python312",
            @"C:\Python311",
            @"C:\Python310",
            @"C:\Python39",
            @"C:\Python38",
        };
        foreach (string baseDir in searchDirs)
        {
            try
            {
                string test = Path.Combine(baseDir, "pythonw.exe");
                if (File.Exists(test))
                    return test;
            }
            catch { }
        }

        // Try where command
        try
        {
            Process p = new Process();
            p.StartInfo.FileName = "where";
            p.StartInfo.Arguments = "pythonw";
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.CreateNoWindow = true;
            p.Start();
            string output = p.StandardOutput.ReadLine();
            p.WaitForExit(3000);
            if (!string.IsNullOrEmpty(output) && File.Exists(output.Trim()))
                return output.Trim();
        }
        catch { }

        return null;
    }
}
