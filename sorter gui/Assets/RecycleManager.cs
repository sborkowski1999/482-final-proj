using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

public class RecycleManager : MonoBehaviour
{
    static Socket listener;
    private CancellationTokenSource source;
    public ManualResetEvent allDone;

    public static readonly int PORT = 1755;
    public static readonly int WAITTIME = 1;

    public GameObject canPrefab;   // Assign the CAN prefab in the Inspector
    public GameObject glassPrefab; // Assign the GLASS prefab in the Inspector
    public GameObject milkPrefab;  // Assign the MILK prefab in the Inspector
    public GameObject petPrefab;   // Assign the PET prefab in the Inspector

    // Start is called before the first frame update
    async void Start()
    {
        await Task.Run(() => ListenEvents());
    }

    private void ListenEvents()
    {
        source = new CancellationTokenSource();
        allDone = new ManualResetEvent(false);

        IPHostEntry ipHostInfo = Dns.GetHostEntry(Dns.GetHostName());
        IPAddress ipAddress = ipHostInfo.AddressList.FirstOrDefault(ip => ip.AddressFamily == AddressFamily.InterNetwork);
        IPEndPoint localEndPoint = new IPEndPoint(ipAddress, PORT);

        listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

        try
        {
            listener.Bind(localEndPoint);
            listener.Listen(10);

            while (!source.Token.IsCancellationRequested)
            {
                allDone.Reset();

                Debug.Log("Waiting for a connection... host: " + ipAddress.MapToIPv4().ToString() + " port: " + PORT);
                listener.BeginAccept(new AsyncCallback(AcceptCallback), listener);

                while (!source.Token.IsCancellationRequested)
                {
                    if (allDone.WaitOne(WAITTIME))
                    {
                        break;
                    }
                }
            }
        }
        catch (Exception e)
        {
            Debug.LogError(e.ToString());
        }
    }

    private void AcceptCallback(IAsyncResult ar)
    {
        Socket listener = (Socket)ar.AsyncState;
        Socket handler = listener.EndAccept(ar);

        allDone.Set();

        StateObject state = new StateObject();
        state.workSocket = handler;
        handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReadCallback), state);
    }

    private void ReadCallback(IAsyncResult ar)
    {
        StateObject state = (StateObject)ar.AsyncState;
        Socket handler = state.workSocket;

        int read = handler.EndReceive(ar);

        if (read > 0)
        {
            state.colorCode.Append(Encoding.ASCII.GetString(state.buffer, 0, read));
            handler.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReadCallback), state);
        }
        else
        {
            if (state.colorCode.Length > 1)
            {
                string content = state.colorCode.ToString();
                Debug.Log($"Read {content.Length} bytes from socket.\n Data : {content}");
                SpawnGameObject(content);
            }
            handler.Close();
        }
    }

    private void SpawnGameObject(string objectType)
    {
        Vector3 spawnPosition = new Vector3(0f, 1f, 0f); // Change the spawn position as needed
        GameObject prefabToSpawn = null;

        switch (objectType)
        {
            case "CAN":
                prefabToSpawn = canPrefab;
                break;
            case "GLASS":
                prefabToSpawn = glassPrefab;
                break;
            case "MILK":
                prefabToSpawn = milkPrefab;
                break;
            case "PET":
                prefabToSpawn = petPrefab;
                break;
            default:
                Debug.LogWarning("Unknown object type received: " + objectType);
                return; // Don't spawn anything for unknown types
        }

        if (prefabToSpawn != null)
        {
            Instantiate(prefabToSpawn, spawnPosition, Quaternion.identity);
        }
    }

    private void OnDestroy()
    {
        source.Cancel();
    }

    public class StateObject
    {
        public Socket workSocket = null;
        public const int BufferSize = 1024;
        public byte[] buffer = new byte[BufferSize];
        public StringBuilder colorCode = new StringBuilder();
    }
}
