package com.example.butlerkamaster;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.design.widget.TabLayout;
import android.support.v4.app.Fragment;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;

import com.example.butlerkamaster.ClientRequestHandler.ClientRequest;
import com.example.butlerkamaster.ui.main.SectionsPagerAdapter;
import com.example.butlerkamaster.SocketHandler.SocketWorker;

//import com.github.nkzawa.socketio.client.Socket;
import java.net.Socket;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

import java.util.List;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.WebSocket;

public class MainActivity extends AppCompatActivity {
    private OkHttpClient client;
    Socket socket;
    String[] mobileArray = {"Android","IPhone","WindowsMobile","Blackberry",
            "WebOS","Ubuntu","Windows7","Max OS X"};
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //setContentView(R.layout.fragment_1);
        SectionsPagerAdapter sectionsPagerAdapter = new SectionsPagerAdapter(this, getSupportFragmentManager());
        ViewPager viewPager = findViewById(R.id.view_pager);
        viewPager.setAdapter(sectionsPagerAdapter);
        final TabLayout tabs = findViewById(R.id.tabs);
        tabs.setupWithViewPager(viewPager);
        FloatingActionButton fab = findViewById(R.id.fab);

        ArrayAdapter adapter = new ArrayAdapter<String>(this,
                R.layout.activity_listview, mobileArray);

        ListView listView = (ListView) findViewById(R.id.mobile_list);
        listView.setAdapter(adapter);

        //setContentView(R.layout.activity_main);
        client = new OkHttpClient();

        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Request request = new Request.Builder().url("http://10.73.151.53:3000/butler").build();// ws://10.73.151.53:3907/butler || ws://echo.websocket.org
                SocketWorker sw = new SocketWorker();
                final WebSocket ws = client.newWebSocket(request, sw);
                int noOfTabs = tabs.getTabCount();
                for(int j=0; j<noOfTabs; j++){
                    Log.e("Main", tabs.getTabAt(j).getText().toString());
                    if(tabs.getTabAt(j).isSelected()){
                        Log.e("Main", "Yes");
                        switch (tabs.getTabAt(j).getText().toString()){
                            case "North Indian":
                                EditText breadText = (EditText)(findViewById(R.id.breadText));
                                Log.e("Main", "breadtext value is "+breadText.getText().toString());
                                break;
                            case "South Indian":
                                EditText idlyText = (EditText)(findViewById(R.id.idlyText));
                                Log.e("Main", "idlyText value is "+idlyText.getText().toString());
                                break;
                            default:
                                Log.e("Main", "Wrong case");
                        }
                    }else {
                        Log.e("Main", "No");
                    }

                }

                // Prepare client auth request message
                //ClientRequest cr = new ClientRequest();
                //byte[] clientauthreq = cr.formAuthReqMsg("", "", "", "" ,"");
                try {
                    //Log.e("Main", new String(clientauthreq, "UTF-8"));
                    JSONObject json = new JSONObject();
                    json.put("name", "gaux");
                    if(ws.send(json.toString())){ //new String(clientauthreq) | new String(clientauthreq, "UTF-8")
                        Log.e("Main", "Went");
                    }else {
                        Log.e("Main", "Didn't went");
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                ws.close(1000, "");
                Snackbar.make(view, "All stuff done. Closing!!!", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
                //client.dispatcher().executorService().shutdown();
            }
        });
    }
}