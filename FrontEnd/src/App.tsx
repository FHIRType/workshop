import Header from "./components/Header";
import {createBrowserRouter, RouterProvider, ScrollRestoration} from "react-router-dom";
import PostData from "./pages/PostData"
import Home from "./pages/Home";

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
           path: "/",
           element: <Home />
         },
         {
            path: "/getdata",
            element: <Home />,
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