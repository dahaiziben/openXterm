using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;

class Program
{
    static void Main()
    {
        string logFile = Path.Combine(Path.GetTempPath(), "OpenXterm_launcher_test.log");
        try
        {
            string exeDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            string pyzPath = Path.Combine(exeDir, "OpenXterm.pyz");
            if (!File.Exists(pyzPath))
                pyzPath = Path.Combine(Directory.GetCurrentDirectory(), "OpenXterm.pyz");
            
            File.WriteAllText(logFile, "exeDir: " + exeDir + "\r\n");
            File.AppendAllText(logFile, "pyzPath: " + pyzPath + "\r\n");
            File.AppendAllText(logFile, "pyz exists: " + File.Exists(pyzPath) + "\r\n");

            string pythonw = FindPythonw();
            File.AppendAllText(logFile, "pythonw: " + (pythonw ?? "null") + "\r\n");
            
            if (pythonw == null || !File.Exists(pyzPath))
                return;

            Process.Start(new ProcessStartInfo
            {
                FileName = pythonw,
                Arguments = "\"" + pyzPath + "\"",
                WorkingDirectory = exeDir,
                UseShellExecute = false,
                CreateNoWindow = true
            });
            File.AppendAllText(logFile, "Launched OK\r\n");
        }
        catch (Exception ex)
        {
            File.AppendAllText(logFile, "ERROR: " + ex.ToString() + "\r\n");
        }
    }

    static string FindPythonw()
    {
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
