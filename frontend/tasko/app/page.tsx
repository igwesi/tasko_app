"use client"
import Link from "next/link";
import { Button } from "@radix-ui/themes";
import { useRouter, usePathname } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const pathname = usePathname()

  if (pathname == "/auth/login") {
    return (
      <div className="flex flex-col w-full gap-2 row-start-2 items-center sm:items-center">
        <h1 className="font-bold">Welcome to Tasko</h1>
        <Button className="btn btn-primary" onClick={() => router.push("/auth/login")}>
          Get Started
        </Button>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-[50vh] w-full gap-2 row-start-2 justify-center items-center sm:items-center">
      <h1 className="font-bold">Welcome to Tasko</h1>
      <Link href={"/auth/login"} className="btn btn-primary">
        Get Started
      </Link>
    </div>  
  );
}
