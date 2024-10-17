"use client";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { ACCESS_TOKEN } from "./constants";


export function middleware(request: NextRequest) {
    const accessToken = null

    if (
        !accessToken 
        && request.nextUrl.pathname !=="/" 
        && request.nextUrl.pathname !=="/auth/login"
    ) {
        return NextResponse.redirect(new URL("/auth/login", request.url));
    }
}

export const config = {
    matcher: ["/((?!api|auth|_next/static|_next/image|.*\\.png$).*)"],
};