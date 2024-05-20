import { createBrowserRouter, RouterProvider, ScrollRestoration } from 'react-router-dom';
import Home from './pages/Home';
import { NextUIProvider } from '@nextui-org/react';
import BasicLayout from './layouts/BasicLayout.tsx';
import About from './pages/About.tsx';

const router = createBrowserRouter([
    {
        path: '/',
        element: (
            <>
                <ScrollRestoration />
                <BasicLayout />
            </>
        ),
        errorElement: <div>4xx error</div>,
        children: [
            {
                path: '/',
                element: <Home />,
            },
            {
                path: '/about',
                element: <About />,
            },
        ],
    },
]);

export default function App() {
    return (
        <NextUIProvider>
            <RouterProvider router={router} />
        </NextUIProvider>
    );
}
