"use client"
import Parse from 'parse/dist/parse.min.js';
import { useEffect, useState } from 'react';

// https://containers.back4app.com/agents/5a471bd4-12cd-41e6-94bf-cd039a004aa5


export default function Home() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    Parse.initialize(
      process.env.NEXT_PUBLIC_PARSE_APPLICATION_ID,
      process.env.NEXT_PUBLIC_PARSE_JAVASCRIPT_KEY
    );

    Parse.serverURL = process.env.NEXT_PUBLIC_PARSE_SERVER_URL;

    const fetchProjects = async () => {
      const Project = Parse.Object.extend('Project');
      const query = new Parse.Query(Project);

      try {
        const results = await query.find();
        setProjects(results);
      } catch (error) {
        console.error('Error while fetching projects', error);
      }
    };

    fetchProjects();
  }, []);

  return (
    <div>
      <div className="text-center mb-4 font-bold text-4xl">Projects</div>

      <div className="">
        <ul>
          {projects.map((project) => (
            <li className="my-2" key={project.id}>
              <span className="font-bold">{project.get('projectName')}:</span> {project.get('description')}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}