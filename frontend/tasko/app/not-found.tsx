'use client';
import { useRouter } from 'next/navigation';
import { Metadata } from "next";
import { Button } from '@radix-ui/themes';
import { Button as HButton } from '@headlessui/react';

// Define metadata for the 404 page
export const metadata: Metadata = {
  title: "Tasko - Not Found",
  description: "Tasko - Not Found",
};


export default function NotFound() {
  const router = useRouter();

  return (
    <div className="absolute left-1/2 top-1/2 mb-16 -translate-x-1/2 -translate-y-1/2 items-center justify-center text-center">
      <span className="bg-gradient-to-b from-foreground to-transparent bg-clip-text text-[10rem] font-extrabold leading-none">
        404
      </span>

      <h2 className="font-heading my-2 text-2xl font-bold">
        Something&apos;s missing
      </h2>
      
      <p>
        Sorry, the page you are looking for doesn&apos;t exist or has been
        moved.
      </p>
      
      <div className="mt-8 flex justify-center gap-2">
        
        <Button className='btn' onClick={() => router.back()}>
          Go back
        </Button>

        <HButton className='btn' onClick={() => router.push('/')}>
          Back to Home
        </HButton>
      </div>
    </div>
  );
}