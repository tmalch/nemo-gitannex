import os
import os.path
import json
import subprocess
import dbus

def  isGitAnnex(directory):
  annexpath = os.path.join(directory,".git/annex")
#  print "check dir " + directory + " for annex in " + annexpath 
  if os.path.exists(annexpath):
    return True
  else:
    if os.path.ismount(directory) or directory == "/":
      return False
    else:
#      print "not found go up to " + os.path.normpath(os.path.join(directory,".."))
      return isGitAnnex(os.path.normpath(os.path.join(directory,"..")))


#os.path.islink(path)  #true if link
#os.path.exists(path)  #false for broken symlink
#os.path.join(os.path.dirname(path), result).

def  isFileLocalAvailable(path):
  if os.path.exists(path):
    return True
  else:
    return False

def  isFileModifyable(path):
  if isFileLocalAvailable(path) and not os.path.islink(path):
    return True
  return False

def lockPath(path):
  loc = os.path.dirname(path)
  name = os.path.basename(path)
  try:
    subprocess.check_output(["/usr/bin/git-annex", "add", name], shell=False, cwd=loc)
    return True
  except subprocess.CalledProcessError as e:
    notify("gitannex lock", str(e))
    print e.output
    return False
  except:
    return False

def unlockPath(path):
  loc = os.path.dirname(path)
  name = os.path.basename(path)
  try:
    subprocess.check_output(["/usr/bin/git-annex","unlock",name],shell=False,cwd=loc)
    return True
  except subprocess.CalledProcessError as e:
    notify("gitannex unlock", str(e))
    print e.output
    return False  
  except:
    return False
    
def getPath(path):
  loc = os.path.dirname(path)
  name = os.path.basename(path)
  try:
    p = subprocess.Popen(["/usr/bin/git-annex","get","--notify-start","--notify-finish",name], cwd=loc)
    return True
  except:
    return False

def dropPath(path):
  loc = os.path.dirname(path)
  name = os.path.basename(path)
  try:
    subprocess.check_output(["/usr/bin/git-annex","drop",name],shell=False,cwd=loc)
    notify("gitannex drop","file "+name+" dropped")
    return True
  except subprocess.CalledProcessError as e:
    notify("gitannex drop", e.output)
    print e.output
    return False   
  except:
    return False

def notify(summary, body='', app_name='', app_icon='',timeout=5000, actions=[], hints=[], replaces_id=0):
  #http://mueller.panopticdev.com/2011/06/create-notification-bubbles-in-python.html
  _bus_name = 'org.freedesktop.Notifications'
  _object_path = '/org/freedesktop/Notifications'
  _interface_name = _bus_name
  session_bus = dbus.SessionBus()
  obj = session_bus.get_object(_bus_name, _object_path)
  interface = dbus.Interface(obj, _interface_name)
  interface.Notify(app_name, replaces_id, app_icon,summary, body, actions, hints, timeout)

def getLocations(path):
  res = []
  loc = os.path.dirname(path)
  name = os.path.basename(path)
  print "get locations for: "+name
  try:
    out = subprocess.check_output(["/usr/bin/git-annex","whereis","--json",name],shell=False,cwd=loc)
    outobj = json.JSONDecoder().decode(out)
  except:
    return res
  if outobj[u'success'] != True:
    return res
  for loc in outobj[u'whereis']:
    if loc[u'here'] == True:
      res.append("here")
    else:
      res.append(loc[u'description'])
  return res

def sync(loc):
  try:
    subprocess.check_output(["/usr/bin/git-annex", "sync"], shell=False, cwd=loc)
    return True
  except subprocess.CalledProcessError as e:
    notify("gitannex sync", str(e))
    print e.output
    return False
  except:
    return False