import sys
paths = sys.path
tool_path = "C:/dev/maya_plugins/moCap_translator_v02"
if tool_path not in paths:
    sys.path.append( tool_path )

import moCap_translator_v02; reload(moCap_translator_v02)
moCap_translator_v02.create()
