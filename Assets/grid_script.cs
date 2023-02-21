using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using System.Globalization;

// // blank background for github
// public class grid_script : MonoBehaviour
// {
//     //public GameObject brick;
//     public GameObject agent;
//     
//     public Camera camera;
//     public GameObject landmark_stone;
//     public GameObject landmark_tree;
//     public GameObject landmark_treetrunk;
//
//     GameObject landmark_stone_temp;
//     GameObject landmark_tree_temp;
//     GameObject landmark_treetrunk_temp;
//
//     GameObject[] landmarks;
//     private CharacterController controller;
//     float minimumVertexDistance = 0.1f;
//     float init_loc_x = 0.0f;
//     float init_loc_y = 0.0f;
//     float next_loc_x = 0.0f;
//     float next_loc_y = 0.0f;
//     static int init_y_agent = 0;
//     
//     static int init_x = 0;
//     static int init_z = 0;
//     static int counter = 0;
//
//     bool passive_move_on = false;
//     bool ready_for_next_step = true;
//     bool passive_move = true;
//
//     Vector3 camera_init_location = new Vector3(240, 50, 240);
//     Vector3 old_location = new Vector3(init_x, init_y_agent, init_z);
//     Vector3 target_location = new Vector3(0, 0, 0);
//     Vector3 camera_rotation = new Vector3(90, 0, 0);
//     
//     static System.Random rnd = new System.Random();
//     
//     void Start()
//     {
//         camera = Instantiate(camera, camera_init_location, Quaternion.identity);
//         camera.transform.Rotate(camera_rotation);
//
//         add_landmark();
//         ScreenCapture.CaptureScreenshot("/Users/bo/Desktop/replay_data/unity_blank_env.jpg", 2);
//     }
//
//     void Update()
//     {
//     }
//
//     void add_landmark()
//     {
//         //setup stone
//         for (int i = 0; i < rnd.Next(250, 400); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_stone_temp = Instantiate(landmark_stone, cur_loc, Quaternion.identity);
//             landmark_stone_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//             landmark_stone_temp.tag = "landmark";
//         }
//         //setup tree
//         for (int i = 0; i < rnd.Next(800, 1500); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_tree_temp = Instantiate(landmark_tree, cur_loc, Quaternion.identity);
//             landmark_tree_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//             landmark_tree_temp.tag = "landmark";
//         }
//         //setup treetrunk
//         for (int i = 0; i < rnd.Next(250, 400); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_treetrunk_temp = Instantiate(landmark_treetrunk, cur_loc, Quaternion.identity);
//             landmark_treetrunk_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//             landmark_treetrunk_temp.tag = "landmark";
//         }
//     }
// }







// 1 trajectories for github 
public class grid_script : MonoBehaviour
{
    //public GameObject brick;
    public GameObject agent;
    public GameObject landmark_stone;
    public GameObject landmark_tree;
    public GameObject landmark_treetrunk;

    GameObject landmark_stone_temp;
    GameObject landmark_tree_temp;
    GameObject landmark_treetrunk_temp;

    public Camera camera;
    GameObject[] landmarks;
    private CharacterController controller;
    float minimumVertexDistance = 0.1f;
    float init_loc_x = 0.0f;
    float init_loc_y = 0.0f;
    float next_loc_x = 0.0f;
    float next_loc_y = 0.0f;

    static int init_x = 0;
    static int init_z = 0;
    static int init_y_agent = 0;
    static int counter = 0;

    Vector3 camera_init_location = new Vector3(240, 50, 240);
    Vector3 old_location = new Vector3(init_x, init_y_agent, init_z);
    Vector3 target_location = new Vector3(0, 0, 0);
    Vector3 camera_rotation = new Vector3(90, 0, 0);

    Animator animator_agent;
    bool passive_move_on = false;
    bool ready_for_next_step = true;
    bool passive_move = true;
    static System.Random rnd = new System.Random();

    //new List<int>(new int[] { 90, 120, 150, 180, 210, 240});
    List<string> coor_x = new List<string>();
    List<string> coor_y = new List<string>();
    //List<double> pause_list = new List<double>(new double[] { 5.0f, 10.0f, 15.0f });


    void Start()
    {
        camera = Instantiate(camera, camera_init_location, Quaternion.identity);
        camera.transform.Rotate(camera_rotation);
        agent = Instantiate(agent, old_location, Quaternion.identity);
        coor_x = new List<string>();
        coor_y = new List<string>();
        coor_x = GetLines("/Users/bo/Desktop/replay_data/singleSubject_replay180reverse_180dir_stepsize3/dir180_coor_first200_github_x.txt");
        coor_y = GetLines("/Users/bo/Desktop/replay_data/singleSubject_replay180reverse_180dir_stepsize3/dir180_coor_first200_github_y.txt");
        add_landmark();
        
        init_loc_x = float.Parse(coor_x[counter], CultureInfo.InvariantCulture.NumberFormat);
        init_loc_y = float.Parse(coor_y[counter], CultureInfo.InvariantCulture.NumberFormat);
        old_location = new Vector3(init_loc_x, init_y_agent, init_loc_y);
        agent.transform.position = old_location;
        
        ScreenCapture.CaptureScreenshot("/Users/bo/Desktop/replay_data/singleSubject_replay180reverse_180dir_stepsize3/plot_dir180_replay"+counter.ToString()+"step.jpg", 2);
    }

    void Update()
    {

        if (ready_for_next_step)
        {
            ready_for_next_step = false;
            next_loc_x = float.Parse(coor_x[counter+1], CultureInfo.InvariantCulture.NumberFormat);
            next_loc_y = float.Parse(coor_y[counter+1], CultureInfo.InvariantCulture.NumberFormat);
            target_location = new Vector3(next_loc_x, 0f, next_loc_y);
            passive_move_on = true;
            // passive_move = true;
        }

        if (passive_move_on)
        {
            agent.transform.LookAt(target_location);
            agent.transform.position = Vector3.MoveTowards(old_location, target_location, 1000000 * Time.deltaTime);
        }

        if (passive_move)
        {
            passive_move = false;
            start_running();
        }

        Vector3 currentPos = agent.transform.position;
        float distance_to_target = Vector3.Distance(currentPos, target_location);
        if (distance_to_target <= minimumVertexDistance & passive_move_on)
        {
            passive_move_on = false;
            old_location = DrawLine(currentPos, old_location);
            if (counter < coor_x.Count-2)
            {
                ScreenCapture.CaptureScreenshot("/Users/bo/Desktop/replay_data/singleSubject_replay180reverse_180dir_stepsize3/plot_dir180_replay"+counter.ToString()+"step.jpg", 2);
                counter = counter + 1;
                
                // stop_running();
                ready_for_next_step = true;
            }
            else
            {
                ScreenCapture.CaptureScreenshot("/Users/bo/Desktop/replay_data/singleSubject_replay180reverse_180dir_stepsize3/plot_dir180_replay"+counter.ToString()+"step.jpg", 2);
                //agent.transform.LookAt(new Vector3(450, init_y_agent, 230));
                //camera.transform.position = agent.transform.position + new Vector3(15, 15, 0);
                //camera.transform.forward = agent.transform.forward * -1;
                stop_running();
            }
        }
    }
    
    void start_running()
    {
        animator_agent = agent.GetComponent<Animator>();
        animator_agent.runtimeAnimatorController = Instantiate(Resources.Load("Gorilla")) as RuntimeAnimatorController;
        animator_agent.SetTrigger("isRunning");
        // UnityEngine.Debug.Log("aa");
    }
    void stop_running()
    {
        animator_agent = agent.GetComponent<Animator>();
        animator_agent.runtimeAnimatorController = Instantiate(Resources.Load("Gorilla")) as RuntimeAnimatorController;
        animator_agent.SetTrigger("isIdle");
    }
    Vector3 DrawLine(Vector3 currentPos, Vector3 old_location)
    {
        GameObject myLine = new GameObject();
        myLine.tag = "lines";
        myLine.transform.position = currentPos;
        myLine.AddComponent<LineRenderer>();
        LineRenderer lr = myLine.GetComponent<LineRenderer>();
        lr.material = new Material(Shader.Find("Sprites/Default"));
        lr.SetColors(Color.black, Color.black);
        lr.SetWidth(0.2f, 0.2f);
        lr.SetPosition(0, old_location);
        lr.SetPosition(1, currentPos);
        //GameObject.Destroy(myLine, duration);
        old_location = currentPos;
        return old_location;
    }
    public static List<string> GetLines(string filename)
    {
        List<string> result = new List<string>(); // A list of strings 
        using (StreamReader reader = new StreamReader(filename))
        {
            string line = string.Empty;
            while ((line = reader.ReadLine()) != null)
            {
                if (line != string.Empty)
                {
                    result.Add(line);
                }
            }
        }
        return result;
    }

    void add_landmark()
    {
        //setup stone
        for (int i = 0; i < rnd.Next(250, 400); i++)
        {
            Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
            landmark_stone_temp = Instantiate(landmark_stone, cur_loc, Quaternion.identity);
            landmark_stone_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
            landmark_stone_temp.tag = "landmark";
        }
        //setup tree
        for (int i = 0; i < rnd.Next(800, 1500); i++)
        {
            Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
            landmark_tree_temp = Instantiate(landmark_tree, cur_loc, Quaternion.identity);
            landmark_tree_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
            landmark_tree_temp.tag = "landmark";
        }
        //setup treetrunk
        for (int i = 0; i < rnd.Next(250, 400); i++)
        {
            Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
            landmark_treetrunk_temp = Instantiate(landmark_treetrunk, cur_loc, Quaternion.identity);
            landmark_treetrunk_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
            landmark_treetrunk_temp.tag = "landmark";
        }
    }
}





// // plot 16 trajectories in one figure 
// public class grid_script : MonoBehaviour
// {
//
//     //public GameObject brick;
//     public GameObject agent;
//     public GameObject landmark_stone;
//     public GameObject landmark_tree;
//     public GameObject landmark_treetrunk;
//
//     GameObject landmark_stone_temp;
//     GameObject landmark_tree_temp;
//     GameObject landmark_treetrunk_temp;
//
//
//     public Camera camera;
//     GameObject[] landmarks;
//     private CharacterController controller;
//     float minimumVertexDistance = 0.1f;
//     float init_loc_x = 0.0f;
//     float init_loc_y = 0.0f;
//     float next_loc_x = 0.0f;
//     float next_loc_y = 0.0f;
//
//     static int init_x = 0;
//     static int init_z = 0;
//     static int init_y_agent = 0;
//     static int counter = 1;
//     int ith_sub = 0;
//     double move_distance = 8.0f;
//
//     Vector3 camera_init_location = new Vector3(240, 40, 240);
//     Vector3 old_location = new Vector3(init_x, init_y_agent, init_z);
//     Vector3 target_location = new Vector3(0, 0, 0);
//     Vector3 camera_rotation = new Vector3(90, 0, 0);
//
//     Animator animator_agent;
//     bool movement_on = false;
//      bool passive_move_on = false;
//      bool ready_for_next_step = true;
//      bool passive_move = true;
//     bool put_landmark = false;
//     bool task_end = false;
//     bool pass_loop = true;
//     static System.Random rnd = new System.Random();
//
//     //new List<int>(new int[] { 90, 120, 150, 180, 210, 240});
//     List<string> coor_x = new List<string>();
//     List<string> coor_y = new List<string>();
//     //List<double> pause_list = new List<double>(new double[] { 5.0f, 10.0f, 15.0f });
//
//
//     void Start()
//     {
//         camera = Instantiate(camera, camera_init_location, Quaternion.identity);
//         camera.transform.Rotate(camera_rotation);
//         agent = Instantiate(agent, old_location, Quaternion.identity);
//     }
//
//     void Update()
//     {
//
//         if (pass_loop)
//         {
//
//             pass_loop = false;
//
//             coor_x = new List<string>();
//             coor_y = new List<string>();
//             counter = 1;
//
//             coor_x = GetLines("/Users/bo/Desktop/replay_data/dir180_coor_noreplay_sub" + ith_sub.ToString() + "_x.txt");
//             coor_y = GetLines("/Users/bo/Desktop/replay_data/dir180_coor_noreplay_sub" + ith_sub.ToString() + "_y.txt");
//
//             init_loc_x = float.Parse(coor_x[0], CultureInfo.InvariantCulture.NumberFormat);
//             init_loc_y = float.Parse(coor_y[0], CultureInfo.InvariantCulture.NumberFormat);
//             old_location = new Vector3(init_loc_x, init_y_agent, init_loc_y);
//
//             agent.transform.position = old_location;
//             ready_for_next_step = true;
//         }
//         
//         if (ready_for_next_step)
//         {
//             ready_for_next_step = false;
//
//             next_loc_x = float.Parse(coor_x[counter], CultureInfo.InvariantCulture.NumberFormat);
//             next_loc_y = float.Parse(coor_y[counter], CultureInfo.InvariantCulture.NumberFormat);
//
//             target_location = new Vector3(next_loc_x, 0f, next_loc_y);
//             passive_move_on = true;
//         }
//         
//         if (passive_move_on)
//          {
//              agent.transform.LookAt(target_location);
//              agent.transform.position = Vector3.MoveTowards(old_location, target_location, 1000000 * Time.deltaTime);
//          }
//
//          if (passive_move)
//          {
//              passive_move = false;
//              start_running();
//          }
//
//         Vector3 currentPos = agent.transform.position;
//         float distance_to_target = Vector3.Distance(currentPos, target_location);
//         if (distance_to_target <= minimumVertexDistance & passive_move_on)
//         {
//             //UnityEngine.Debug.Log(counter);
//             old_location = DrawLine(currentPos, old_location);
//             if (counter < coor_x.Count - 1)
//             {
//                 counter = counter + 1;
//                 passive_move_on = false;
//                 stop_running();
//                 ready_for_next_step = true;
//             }
//             else
//             {
//                 passive_move_on = false;
//                 //agent.transform.LookAt(new Vector3(450, init_y_agent, 230));
//                 //camera.transform.position = agent.transform.position + new Vector3(15, 15, 0);
//                 //camera.transform.forward = agent.transform.forward * -1;
//                 stop_running();
//                 
//                 if (ith_sub < 15)
//                 {
//                     ith_sub = ith_sub + 1;
//                     pass_loop = true;
//                 }
//                 else {
//                     // add_landmark();
//                     ScreenCapture.CaptureScreenshot("/Users/bo/Desktop/replay_data/unity_dir180_plot_noreplay.png", 2);
//                 }
//
//             }
//
//         }
//     }
//
//     void start_running()
//     {
//         animator_agent = agent.GetComponent<Animator>();
//         animator_agent.runtimeAnimatorController = Instantiate(Resources.Load("Gorilla")) as RuntimeAnimatorController;
//         animator_agent.SetTrigger("isRunning");
//     }
//     void stop_running()
//     {
//         animator_agent = agent.GetComponent<Animator>();
//         animator_agent.runtimeAnimatorController = Instantiate(Resources.Load("Gorilla")) as RuntimeAnimatorController;
//         animator_agent.SetTrigger("isIdle");
//     }
//     Vector3 DrawLine(Vector3 currentPos, Vector3 old_location)
//     {
//         GameObject myLine = new GameObject();
//         myLine.tag = "lines";
//         myLine.transform.position = currentPos;
//         myLine.AddComponent<LineRenderer>();
//         LineRenderer lr = myLine.GetComponent<LineRenderer>();
//         lr.material = new Material(Shader.Find("Sprites/Default"));
//         lr.SetColors(Color.black, Color.black);
//         lr.SetWidth(0.3f, 0.3f);
//         lr.SetPosition(0, old_location);
//         lr.SetPosition(1, currentPos);
//         //GameObject.Destroy(myLine, duration);
//         old_location = currentPos;
//         return old_location;
//     }
//     public static List<string> GetLines(string filename)
//     {
//         List<string> result = new List<string>(); // A list of strings 
//         using (StreamReader reader = new StreamReader(filename))
//         {
//             string line = string.Empty;
//             while ((line = reader.ReadLine()) != null)
//             {
//                 if (line != string.Empty)
//                 {
//                     result.Add(line);
//                 }
//             }
//         }
//         return result;
//     }
//
//     void add_landmark()
//     {
//         //setup stone
//         for (int i = 0; i < rnd.Next(300, 500); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_stone_temp = Instantiate(landmark_stone, cur_loc, Quaternion.identity);
//             landmark_stone_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//             landmark_stone_temp.tag = "landmark";
//         }
//         //setup tree
//         for (int i = 0; i < rnd.Next(800, 1500); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_tree_temp = Instantiate(landmark_tree, cur_loc, Quaternion.identity);
//             landmark_tree_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//             landmark_tree_temp.tag = "landmark";
//         }
//         //setup treetrunk
//         for (int i = 0; i < rnd.Next(300, 500); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_treetrunk_temp = Instantiate(landmark_treetrunk, cur_loc, Quaternion.identity);
//             landmark_treetrunk_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//             landmark_treetrunk_temp.tag = "landmark";
//         }
//
//     }
// }







// // 16 trajectories for fig.s with each independent 
// public class grid_script : MonoBehaviour
// {
//
//     //public GameObject brick;
//     public GameObject agent;
//     public GameObject landmark_stone;
//     public GameObject landmark_tree;
//     public GameObject landmark_treetrunk;
//
//     GameObject landmark_stone_temp;
//     GameObject landmark_tree_temp;
//     GameObject landmark_treetrunk_temp;
//
//     public Camera camera;
//     GameObject[] landmarks;
//     private CharacterController controller;
//     float minimumVertexDistance = 0.1f;
//     float init_loc_x = 0.0f;
//     float init_loc_y = 0.0f;
//     float next_loc_x = 0.0f;
//     float next_loc_y = 0.0f;
//
//     static int init_x = 0;
//     static int init_z = 0;
//     static int init_y_agent = 0;
//     static int counter = 1;
//     int ith_sub = 0;
//     double move_distance = 8.0f;
//
//     Vector3 camera_init_location = new Vector3(240, 45, 240);
//     Vector3 old_location = new Vector3(init_x, init_y_agent, init_z);
//     Vector3 target_location = new Vector3(0, 0, 0);
//     Vector3 camera_rotation = new Vector3(90, 0, 0);
//
//     Animator animator_agent;
//     bool movement_on = false;
//     bool passive_move_on = false;
//     bool ready_for_next_step = false;
//     bool put_landmark = false;
//     bool task_end = false;
//     bool pass_loop = true;
//     static System.Random rnd = new System.Random();
//
//     //new List<int>(new int[] { 90, 120, 150, 180, 210, 240});
//     List<string> coor_x = new List<string>();
//     List<string> coor_y = new List<string>();
//     //List<double> pause_list = new List<double>(new double[] { 5.0f, 10.0f, 15.0f });
//
//
//     void Start()
//     {
//         camera = Instantiate(camera, camera_init_location, Quaternion.identity);
//         camera.transform.Rotate(camera_rotation);
//         agent = Instantiate(agent, old_location, Quaternion.identity);
//     }
//
//     void Update()
//     {
//
//         if (pass_loop)
//         {
//             landmarks = GameObject.FindGameObjectsWithTag("lines");
//             for (var i = 0; i < landmarks.Length; i++)
//             {
//                 Destroy(landmarks[i]);
//             }
//             landmarks = GameObject.FindGameObjectsWithTag("landmark");
//             for (var i = 0; i < landmarks.Length; i++)
//             {
//                 Destroy(landmarks[i]);
//             }
//
//             pass_loop = false;
//
//             coor_x = new List<string>();
//             coor_y = new List<string>();
//             counter = 1;
//
//             coor_x = GetLines("/Users/bo/Desktop/replay_data/dir180_coor_noreplay_sub" + ith_sub.ToString() + "_x.txt");
//             coor_y = GetLines("/Users/bo/Desktop/replay_data/dir180_coor_noreplay_sub" + ith_sub.ToString() + "_y.txt");
//
//             init_loc_x = float.Parse(coor_x[0], CultureInfo.InvariantCulture.NumberFormat);
//             init_loc_y = float.Parse(coor_y[0], CultureInfo.InvariantCulture.NumberFormat);
//             old_location = new Vector3(init_loc_x, init_y_agent, init_loc_y);
//
//             agent.transform.position = old_location;
//             ready_for_next_step = true;
//
//         }
//
//
//         if (ready_for_next_step)
//         {
//             ready_for_next_step = false;
//
//             next_loc_x = float.Parse(coor_x[counter], CultureInfo.InvariantCulture.NumberFormat);
//             next_loc_y = float.Parse(coor_y[counter], CultureInfo.InvariantCulture.NumberFormat);
//
//             target_location = new Vector3(next_loc_x, 0f, next_loc_y);
//             passive_move_on = true;
//         }
//
//         if (passive_move_on)
//         {
//             controller = agent.GetComponent<CharacterController>();
//             agent.transform.position = Vector3.MoveTowards(old_location, target_location, 1500000 * Time.deltaTime);
//             start_running();
//         }
//
//         Vector3 currentPos = agent.transform.position;
//         float distance_to_target = Vector3.Distance(currentPos, target_location);
//         if (distance_to_target <= minimumVertexDistance & passive_move_on)
//         {
//             //UnityEngine.Debug.Log(counter);
//             old_location = DrawLine(currentPos, old_location);
//             if (counter < coor_x.Count - 1)
//             {
//                 counter = counter + 1;
//                 passive_move_on = false;
//                 stop_running();
//                 ready_for_next_step = true;
//             }
//             else
//             {
//                 passive_move_on = false;
//                 //agent.transform.LookAt(new Vector3(450, init_y_agent, 230));
//                 //camera.transform.position = agent.transform.position + new Vector3(15, 15, 0);
//                 //camera.transform.forward = agent.transform.forward * -1;
//                 stop_running();
//                 add_landmark();
//                 ScreenCapture.CaptureScreenshot("/Users/bo/Desktop/replay_data/dir180_plot_noreplay_sub" + ith_sub.ToString() + ".png", 2);
//
//                 if (ith_sub < 15)
//                 {
//                     ith_sub = ith_sub + 1;
//                     pass_loop = true;
//                 }
//             }
//         }
//     }
//
//     void start_running()
//     {
//         animator_agent = agent.GetComponent<Animator>();
//         animator_agent.runtimeAnimatorController = Instantiate(Resources.Load("Gorilla")) as RuntimeAnimatorController;
//         animator_agent.SetTrigger("isRunning");
//     }
//     void stop_running()
//     {
//         animator_agent = agent.GetComponent<Animator>();
//         animator_agent.runtimeAnimatorController = Instantiate(Resources.Load("Gorilla")) as RuntimeAnimatorController;
//         animator_agent.SetTrigger("isIdle");
//     }
//     Vector3 DrawLine(Vector3 currentPos, Vector3 old_location)
//     {
//         GameObject myLine = new GameObject();
//         myLine.tag = "lines";
//         myLine.transform.position = currentPos;
//         myLine.AddComponent<LineRenderer>();
//         LineRenderer lr = myLine.GetComponent<LineRenderer>();
//         lr.material = new Material(Shader.Find("Sprites/Default"));
//         lr.SetColors(Color.black, Color.black);
//         lr.SetWidth(0.5f, 0.5f);
//         lr.SetPosition(0, old_location);
//         lr.SetPosition(1, currentPos);
//         //GameObject.Destroy(myLine, duration);
//         old_location = currentPos;
//         return old_location;
//     }
//     public static List<string> GetLines(string filename)
//     {
//         List<string> result = new List<string>(); // A list of strings 
//         using (StreamReader reader = new StreamReader(filename))
//         {
//             string line = string.Empty;
//             while ((line = reader.ReadLine()) != null)
//             {
//                 if (line != string.Empty)
//                 {
//                     result.Add(line);
//                 }
//             }
//         }
//         return result;
//     }
//
//     void add_landmark()
//     {
//         //setup stone
//         for (int i = 0; i < rnd.Next(200, 400); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_stone_temp = Instantiate(landmark_stone, cur_loc, Quaternion.identity);
//             landmark_stone_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//             landmark_stone_temp.tag = "landmark";
//         }
//         //setup tree
//         for (int i = 0; i < rnd.Next(800, 1500); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_tree_temp = Instantiate(landmark_tree, cur_loc, Quaternion.identity);
//             landmark_tree_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//             landmark_tree_temp.tag = "landmark";
//         }
//         //setup treetrunk
//         for (int i = 0; i < rnd.Next(200, 400); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_treetrunk_temp = Instantiate(landmark_treetrunk, cur_loc, Quaternion.identity);
//             landmark_treetrunk_temp.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//             landmark_treetrunk_temp.tag = "landmark";
//         }
//
//     }
// }









// // perspective view for 1 trajectory
// public class grid_script : MonoBehaviour
// {
//
//     //public GameObject brick;
//     public GameObject agent;
//     public GameObject landmark_stone;
//     public GameObject landmark_tree;
//     public GameObject landmark_treetrunk;
//     GameObject[] landmarks;
//     public Camera camera;
//     public LineRenderer Line;
//     private CharacterController controller;
//     float minimumVertexDistance = 0.1f;
//     float init_loc_x = 0.0f;
//     float init_loc_y = 0.0f;
//     float next_loc_x = 0.0f;
//     float next_loc_y = 0.0f;
//
//     static int init_x = 0;
//     static int init_z = 0;
//     static int init_y_agent = 0;
//     static int counter = 1;
//     double move_distance = 8.0f;
//
//     Vector3 camera_init_location = new Vector3(225, 80, 225);
//     Vector3 old_location = new Vector3(init_x, init_y_agent, init_z);
//     Vector3 target_location = new Vector3(0, 0, 0);
//     Vector3 camera_rotation = new Vector3(90, 0, 0);
//
//     Animator animator_agent;
//     bool movement_on = false;
//     bool passive_move_on = false;
//     bool ready_for_next_step = true;
//     bool put_landmark = false;
//     bool task_end = false;
//     static System.Random rnd = new System.Random();
//
//     //new List<int>(new int[] { 90, 120, 150, 180, 210, 240});
//     List<string> coor_x = new List<string>();
//     List<string> coor_y = new List<string>();
//
//     private IEnumerator coroutine;
//     void Start()
//     {
//         coor_x = GetLines("/Users/bo/Desktop/replay_data/unity_traj_example_x.txt");
//         coor_y = GetLines("/Users/bo/Desktop/replay_data/unity_traj_example_y.txt");
//
//         init_loc_x = float.Parse(coor_x[0], CultureInfo.InvariantCulture.NumberFormat);
//         init_loc_y = float.Parse(coor_y[0], CultureInfo.InvariantCulture.NumberFormat);
//         old_location = new Vector3(init_loc_x, init_y_agent, init_loc_y);
//
//         agent = Instantiate(agent, old_location, Quaternion.identity);
//
//         camera = Instantiate(camera, new Vector3(250, 10, 230), Quaternion.identity);
//         camera.transform.rotation = Quaternion.Euler(new Vector3(35, -130, 0));
//     }
//
//
//     void Update()
//     {
//         if (ready_for_next_step)
//         {
//             ready_for_next_step = false;
//             next_loc_x = float.Parse(coor_x[counter], CultureInfo.InvariantCulture.NumberFormat);
//             next_loc_y = float.Parse(coor_y[counter], CultureInfo.InvariantCulture.NumberFormat);
//             target_location = new Vector3(next_loc_x, 0f, next_loc_y);
//             passive_move_on = true;
//         }
//
//         if (passive_move_on)
//         {
//             controller = agent.GetComponent<CharacterController>();
//             agent.transform.position = Vector3.MoveTowards(old_location, target_location, 1500000 * Time.deltaTime);
//             start_running();
//         }
//
//         Vector3 currentPos = agent.transform.position;
//         float distance_to_target = Vector3.Distance(currentPos, target_location);
//         if (distance_to_target <= minimumVertexDistance & !task_end)
//         {
//             //UnityEngine.Debug.Log(counter);
//             old_location = DrawLine(currentPos, old_location);
//             if (counter < coor_x.Count - 1)
//             {
//                 counter = counter + 1;
//                 passive_move_on = false;
//                 stop_running();
//                 ready_for_next_step = true;
//             }
//             else
//             {
//                 
//                 passive_move_on = false;
//                 task_end = true;
//                 stop_running();
//                 add_landmark();
//                 ScreenCapture.CaptureScreenshot("/Users/bo/Desktop/ss1.png", 2);
//                 
//                 coroutine = WaitAndPrint(2.0f);
//                 StartCoroutine(coroutine);
//             }
//         }
//         
//
//     }
//
//
//     // every 2 seconds perform the print()
//     private IEnumerator WaitAndPrint(float waitTime)
//     {
//         while (true)
//         {
//             yield return new WaitForSeconds(waitTime);
//             print("WaitAndPrint " + Time.time);
//             // landmarks = GameObject.FindGameObjectsWithTag("lines");
//             // for (var i = 0; i < landmarks.Length; i++)
//             // {
//             //     Destroy(landmarks[i]);
//             // }
//             camera.transform.position = new Vector3(old_location.x, 30, old_location.z);
//             camera.transform.rotation = Quaternion.Euler(new Vector3(90, 0, 0));
//             ScreenCapture.CaptureScreenshot("/Users/bo/Desktop/ss2.png", 2);
//         }
//     }
//     
//     void start_running()
//     {
//         animator_agent = agent.GetComponent<Animator>();
//         animator_agent.runtimeAnimatorController = Instantiate(Resources.Load("Gorilla")) as RuntimeAnimatorController;
//         animator_agent.SetTrigger("isRunning");
//     }
//     void stop_running()
//     {
//         animator_agent = agent.GetComponent<Animator>();
//         animator_agent.runtimeAnimatorController = Instantiate(Resources.Load("Gorilla")) as RuntimeAnimatorController;
//         animator_agent.SetTrigger("isIdle");
//     }
//     Vector3 DrawLine(Vector3 currentPos, Vector3 old_location)
//     {
//         GameObject myLine = new GameObject();
//         myLine.tag = "lines";
//         myLine.transform.position = currentPos;
//         myLine.AddComponent<LineRenderer>();
//         LineRenderer lr = myLine.GetComponent<LineRenderer>();
//         lr.material = new Material(Shader.Find("Sprites/Default"));
//         lr.SetColors(Color.black, Color.black);
//         lr.SetWidth(0.2f, 0.2f);
//         lr.SetPosition(0, old_location);
//         lr.SetPosition(1, currentPos);
//         //GameObject.Destroy(myLine, duration);
//         old_location = currentPos;
//         return old_location;
//     }
//     public static List<string> GetLines(string filename)
//     {
//         List<string> result = new List<string>(); // A list of strings 
//         using (StreamReader reader = new StreamReader(filename))
//         {
//             string line = string.Empty;
//             while ((line = reader.ReadLine()) != null)
//             {
//                 if (line != string.Empty)
//                 {
//                     result.Add(line);
//                 }
//             }
//         }
//         return result;
//     }
//
//     void add_landmark()
//     {
//         //setup stone
//         for (int i = 0; i < rnd.Next(100, 400); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_stone = Instantiate(landmark_stone, cur_loc, Quaternion.identity);
//             landmark_stone.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//         }
//         //setup tree
//         for (int i = 0; i < rnd.Next(500, 1300); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_tree = Instantiate(landmark_tree, cur_loc, Quaternion.identity);
//             landmark_tree.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//         }
//         //setup treetrunk
//         for (int i = 0; i < rnd.Next(300, 500); i++)
//         {
//             Vector3 cur_loc = new Vector3(rnd.Next(20, 460), init_y_agent, rnd.Next(20, 460));
//             landmark_treetrunk = Instantiate(landmark_treetrunk, cur_loc, Quaternion.identity);
//             landmark_treetrunk.transform.Rotate(new Vector3(0, rnd.Next(-180, 180), 0));
//         }
//
//     }
//
// }
