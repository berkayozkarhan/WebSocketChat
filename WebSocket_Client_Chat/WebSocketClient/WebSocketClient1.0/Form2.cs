using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WebSocketClient1._0
{
    public partial class Form2 : Form
    {
        ClientWebSocket socket = new ClientWebSocket();
       
        



        public Form2()
        {
            InitializeComponent();
            richTextBoxReceiveMsg.Text += "Ready to connect.";
        }

        private  void Form2_Load(object sender, EventArgs e)
        {
            //listView1.Columns.Add("Nick Name",95);
            //listView1.Columns.Add("Status",100);
            //listView1.Columns.Add("UID", 100);
            

        }

        private async void buttonConnect_Click(object sender, EventArgs e)
        {
            buttonConnect.Text = "Connecting..";
            buttonConnect.Enabled = false;
            
            String connectionUrl = "ws://" + textBoxServerAdress.Text + ":" + textBoxServerPort.Text;
            FirstMessage firstMessage = new FirstMessage();
            firstMessage.user_name = textBoxUserName.Text;
            firstMessage.message_type = "first-connection";
            firstMessage.message = "Hello.I am " + textBoxUserName.Text;
            string firstmessageJSON = JsonConvert.SerializeObject(firstMessage);
            await socket.ConnectAsync(new Uri(connectionUrl), CancellationToken.None);                         
            if(socket.State == WebSocketState.Open)
            {
                //Interface yaklaşımıyla yapılabilir.
                richTextBoxReceiveMsg.Text += "\nConnection Opened.Server Adress:" + textBoxServerAdress.Text;
                buttonConnect.Text = "Connected.";
                richTextBoxSendMsg.Enabled = true;
                buttonDisconnect.Enabled = true;
                buttonSend.Enabled = true;
                //Interface yaklaşımı ile yapılabilir.
                ArraySegment<byte> bufferSend = new ArraySegment<byte>(Encoding.UTF8.GetBytes(firstmessageJSON));
                await Send(socket, bufferSend);
                await ReceiveMessage(socket, async (result, buffer) =>
                 {
                     
                     if (result.MessageType == WebSocketMessageType.Text)
                     {
                         //Online kullanıcıları burada kontrol edeceğiz.
                         string data = Encoding.UTF8.GetString(buffer, 0, result.Count);
                         Message incoming = JsonConvert.DeserializeObject<Message>(data);
                         //Serverden gelen verinin ne tür bir bildiri olduğu burada kontrol edilir.-Berkay
                         switch (incoming.message_type)
                         {
                             case "online-clients":
                                 //richTextBoxReceiveMsg.Text += $"\nOnline Clients Information received:\n" + incoming.message;
                                 List<Client> online_clients = JsonConvert.DeserializeObject<List<Client>>(incoming.message);
                                 //bool kayitKontrol = false;
                                 listView1.Items.Clear();
                                 foreach (Client element in online_clients)
                                 {
                                     String[] bilgiler = { element.username,element.status,element.user_ID};
                                     ListViewItem lst = new ListViewItem(bilgiler);
                                     if (element.username != textBoxUserName.Text)
                                     {
                                         listView1.Items.Add(lst);
                                     }   

                                 }
                                 break;
                             case "welcome-message":
                                 richTextBoxReceiveMsg.Text += $"\n" + incoming.message;
                                 break;
                             case "directed-message":
                                 richTextBoxReceiveMsg.Text += $"\n" + incoming._from + ":" + incoming.message;

                                 break;
                             case "broadcast":
                                 richTextBoxReceiveMsg.Text += $"\n" + incoming.message;
                                 break;
                             default:
                                 break;

                         }
                         
                         //richTextBoxReceiveMsg.Text += $"\n{Encoding.UTF8.GetString(buffer,0,result.Count)}";
                         return;
                     }
                     else if (result.MessageType == WebSocketMessageType.Close)
                     {
                        richTextBoxReceiveMsg.Text += "\nReceived Close Message.";
                         return;
                     }
                 });
            }
           

        }


        
        private async void buttonDisconnect_Click(object sender, EventArgs e)
        {
            await socket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing from the client", CancellationToken.None);
            socket.Abort();
            socket = new ClientWebSocket();
            richTextBoxReceiveMsg.Text = "";
            richTextBoxReceiveMsg.Text += "Bağlantı sonlandırıldı.";
            buttonDisconnect.Enabled = false;
            buttonConnect.Enabled = true;
            richTextBoxSendMsg.Enabled = false;
            buttonSend.Enabled = false;
            listView1.Items.Clear();
            buttonConnect.Text = "Connect";

        }

        private async void buttonSend_Click(object sender, EventArgs e)
        {
            if(socket.State != WebSocketState.Open)
            {
                MessageBox.Show("Socket is not open.", "ALERT!", MessageBoxButtons.OK);
            }
            else
            {
                Message msg = new Message();

                msg.message_type = "broadcast";
                msg._from = textBoxUserName.Text;
                msg._to = "everyone";
                if (richTextBoxSendMsg.Text=="")
                {
                    return;
                }
                else
                {
                    msg.message = richTextBoxSendMsg.Text;
                }
                

                String msgJSON = JsonConvert.SerializeObject(msg);
                ArraySegment<byte> buffer = new ArraySegment<byte>(Encoding.UTF8.GetBytes(msgJSON));
                await Send(socket, buffer);
                richTextBoxSendMsg.Clear();
                
            }
        }

        static async Task Send(ClientWebSocket socket, ArraySegment<byte> data) =>
            await socket.SendAsync(data, WebSocketMessageType.Text, true, CancellationToken.None);


        private async Task ReceiveMessage(WebSocket socket,Action<WebSocketReceiveResult,byte[]> handleMessage)
        {
            
            var buffer = new byte[1024 * 4];
            while(socket.State == WebSocketState.Open)
            {
                var result = await socket.ReceiveAsync(buffer: new ArraySegment<byte>(buffer),
                    CancellationToken.None);
                handleMessage(result, buffer); 
            }
        }

        static void ListUsers(List<Client> online_clients)
        {
            foreach(Client element in online_clients )
            {
                
            }
        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {
            MessageBox.Show(listView1.Items.ToString());
            
        }
    }
}
