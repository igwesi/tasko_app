import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Tasko",
  description: "Tasko",
  appleWebApp: {
    title: "Tasko",
    capable: true,
    statusBarStyle: "default",
  }
}

import Theme from "../components/Theme";
import Navbar from "@/components/Navbar";

export default function RootLayout({children,}: Readonly<{
  children: React.ReactNode;
}>) {
  
  return (
    <html lang="en" data-theme="emerald">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <div className="flex flex-col items-center justify-items-center min-h-screen max-h-screen p-8 pb-8 gap-20 font-[family-name:var(--font-geist-sans)]">       
          <div className="flex flex-row w-full justify-between items-center">
            <div className="items-start my-auto">
              <Navbar/>
            </div>
            <div className="items-end my-auto">
              <Theme/>
            </div>
          </div>
          
          <main className="flex flex-row w-full items-center justify-center">
            {children}
          </main>

          <footer className="row-start-3 gap-6 absolute bottom-10">
            <div className="flex row-start-4 gap-4">
              <a
                href="https://github.com/igwesi/Tasko"
                className="text-sm hover:underline"
                target="_blank"
              >
                Powered by Tasko
              </a>

              <a
                href="https://github.com/igwesi"
                className="text-sm hover:underline"
                target="_blank"
              >
                Created by @igwesi
              </a>
              <a
                href="https://github.com/igwesi/Tasko/blob/main/LICENSE"
                className="text-sm hover:underline"
                target="_blank"
              >
                MIT License
              </a>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
