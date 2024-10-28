"use client"
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col h-[50vh] w-full gap-2 row-start-2 justify-center items-center sm:items-center">
      <h1 className="font-bold">Welcome to Tasko</h1>
      <Link href={"/dashboard"} className="btn btn-primary">
        Get Started
      </Link>
    </div>  
  );
}
