import Header from "./components/Header";
import {createBrowserRouter, RouterProvider, ScrollRestoration} from "react-router-dom";
import GetData from "./pages/GetData";
import PostData from "./pages/PostData"

const router = createBrowserRouter( [
   {
      path: "/",
      element: (
         <>
            <ScrollRestoration />
            <Header />
         </>
      ),
      errorElement: (
         <div>
            4xx error
         </div>
      ),
      children: [
         {
            path: "/getdata",
            element: <GetData />,
         },
         {
            path: "/postdata",
            element: <PostData/>,
         }
      ]
   }
])

export default function App () {
   return (
       <RouterProvider router={router} />
   );
};