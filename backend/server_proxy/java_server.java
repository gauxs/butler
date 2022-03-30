import com.example.butlerkamaster.FlatbufferDefs.ServerProxy.Header;
import com.example.butlerkamaster.FlatbufferDefs.ServerProxy.ProxyMsg;
import com.google.flatbuffers.FlatBufferBuilder;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import com.google.common.io.ByteStreams;

public class JavaServer {
    public static void main(String[] args) throws IOException, NoSuchAlgorithmException {
        ServerSocket server = new ServerSocket(3907);
        try {
            System.out.println("Server has started on port 3907/butler.\r\nWaiting for a connection..."); //ws://10.73.151.53:3907/butler
            Socket client = server.accept();
            System.out.println("A client connected.");
            InputStream in = client.getInputStream();
            ByteBuffer bb = ByteBuffer.wrap(IOUtils.toByteArray(in));

            ProxyMsg proxy_msg = ProxyMsg.getRootAsProxyMsg(bb);
            Header header = proxy_msg.header();
            System.out.println("Country",header.country());
        } catch (Exception e) {
        }
    }
}