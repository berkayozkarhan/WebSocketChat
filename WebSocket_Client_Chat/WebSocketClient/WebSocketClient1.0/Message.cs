using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WebSocketClient1._0
{
    class Message //FirstMessage ile arasında kalıtım ile aktarılabilecek öğeler mevcut.
    {
        public string message_type { get; set; }
        public string _from { get; set; }
        public string _to { get; set; }
        public string message { get; set; }
        public string date { get; set; }

        

    }
}
