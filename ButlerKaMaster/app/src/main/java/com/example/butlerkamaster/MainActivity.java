package com.example.butlerkamaster;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.design.widget.TabLayout;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;

import com.example.butlerkamaster.ui.main.SectionsPagerAdapter;
import com.example.butlerkamaster.ui.main.SocketWorker;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okio.ByteString;

public class MainActivity extends AppCompatActivity {
    private OkHttpClient client;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        SectionsPagerAdapter sectionsPagerAdapter = new SectionsPagerAdapter(this, getSupportFragmentManager());
        ViewPager viewPager = findViewById(R.id.view_pager);
        viewPager.setAdapter(sectionsPagerAdapter);
        TabLayout tabs = findViewById(R.id.tabs);
        tabs.setupWithViewPager(viewPager);
        FloatingActionButton fab = findViewById(R.id.fab);

        client = new OkHttpClient();
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Request request = new Request.Builder().url("ws://10.73.151.53:3907/butler").build();////ws://10.73.151.53:3907 ws://echo.websocket.org
                SocketWorker sw = new SocketWorker();
                WebSocket ws = client.newWebSocket(request, sw);
                ws.send("Hello");
                Snackbar.make(view, "All stuff done. Closing!!!", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
                client.dispatcher().executorService().shutdown();
            }
        });
    }
}